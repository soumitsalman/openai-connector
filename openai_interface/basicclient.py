from functools import reduce
import openai
import tiktoken
import json
import config
from openai_interface.retryutils import retry_after_random_wait
import openai_interface.tokenutils as tok

class BasicClient:
    def __init__(self, api_key: str, org_id: str = None, instructions: [str] = None, functions = None):
        self.openai_client = openai.OpenAI(api_key=api_key, organization=org_id)
        self.model = config.get_basic_model()
        self.instructions = instructions
        self.thread = []
        self._reset_window()

    def _reset_window(self):
        if self.instructions != None:
            self.thread = [_create_message("system", inst) for inst in self.instructions]
        else:
            self.thread = []

    def _count_tokens_in_thread(self) -> int:
        # this is using approximation of the content messages only and not counting the function call
        tcounts = [tok.count_tokens(m["content"], self.model) for m in self.thread if ("content" in m)]
        return reduce((lambda a,b: a+b), tcounts)

    # adds to the thread and clears up the context window before that so that openai API doesnt die
    def _add_to_thread(self, msg):      
        # if msg is not framed as { "role": "<role>", "content": "<content>" } then msg is likely a ChatCompletionMessage returned by the assistant
        # for assistant messages just add the message. The context window is fine since it returned a message anyway
        if isinstance(msg, dict):
            exceed_context_window = lambda msg: (
                self._count_tokens_in_thread()
                + tok.count_tokens(msg["content"], self.model)) >= config.get_openai_chat_context_window()
            if (msg["role"] == "user") and exceed_context_window(msg):
                # print("[DEBUG MSG] Resetting context window for: ", msg)
                self._reset_window()
        self.thread.append(msg)

    @retry_after_random_wait(min_wait=61, max_wait=240, retry_count=5, errors=(openai.RateLimitError))
    def send(self, msg: str):
        #this takes care of the context window if it gets bigger. DO NOT ADD directly to the thread
        self._add_to_thread(_create_message("user", msg))
        results = self.openai_client.chat.completions.create(
            model = self.model,
            messages = self.thread,
            temperature = 0.4,
            seed = 10000 #random number to keep the response consistent
        )
        resp = results.choices[0].message
        # response messages can be added to the context window since if the window was larger it would failed anyway
        self._add_to_thread(resp)

        # TODO: remove this. this entirely for debug and fine-tuning
        # print("[USER]", msg)
        # print("[OPENAI] ", resp.content)

        return resp.content 
    
    # batches multiple items in the msgs that will fit in one message token limit and sends it. This is primarily for efficiency
    # prompt is an optional parameter that is message which will be prefixed infront of every batch
    def send_batch(self, msgs: list[str], prompt: str = None):
        #this will likely blow through the context window size. So reset to begin with
        self._reset_window()
        # create the batched message and run for each batch with the prompt (if there is any)
        for msg in _create_batches(self.model, msgs):
            # prefix the prompt
            if prompt != None:
                self._add_to_thread(_create_message("user", prompt))
            yield self.send(msg) 



#internal utility function for creating a message format for openai client
def _create_message(role: str, msg: str) -> dict[str, str]:
    return {"role": role, "content": msg}

#takes the list of items and bulks a bunch of them in the same message without blowing through the max_msg_tokens
#prompt is an optional parameter. This is added as a padding to each of the bulk messages. Primarily use to ensure context through out batched messages
def _create_batches(model: str, items: list[str]):
    # only process if the current message size <= max_msg_tokens
    # if a message is larger than the max token length then it wont fit by itself anyway
    # another option is to split it in half?
    items = [msg for msg in items if tok.count_tokens(content=msg, model=model) <= config.get_openai_max_msg_tokens()]
    token_counts = [tok.count_tokens(content=msg, model=model) for msg in items]

    cursor = 0
    for i in range(len(token_counts)):
        add_int = lambda a, b: a+b
        cur_tcount = reduce(add_int, token_counts[cursor:i+1])
        # print("[DEBUG MSG] cursor=%d | i=%d | cur_tcount=%d" % (cursor, i+1, cur_tcount))
        # if adding the current item exceeds the max_msg_token OR we are at the last item anyway then package and send
        if cur_tcount > config.get_openai_max_msg_tokens() or (i == len(token_counts)-1):            
            yield "\n\n".join(items[cursor:i+1]) 
            cursor = i+1