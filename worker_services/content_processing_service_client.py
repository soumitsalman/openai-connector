import json
import config
from openai_interface.basicclient import BasicClient

# service client
class ContentProcessingServiceClient:
    # TODO: check is user_id even needed
    def __init__(self, user_id: str, instructions, prompt, collect_func, save_func):
        self.user_id = user_id
        #self.instructions = instructions
        self.prompt = prompt
        self.client = BasicClient(
            api_key=config.get_openai_api_key(),
            org_id=config.get_openai_org_id(),
            instructions=instructions
        )
        self.collect_func = collect_func
        self.save_func = save_func

    def run(self):
        # collect data
        contents = self.collect_func()
        print("[DEBUG MSG] Items being filtered:\n", contents)

        filtered_items = []
        #process each item as they come back
        for resp in self.client.send_batch(msgs = [json.dumps(c) for c in contents], prompt = self.prompt):
            #remove the leading and trailing whitespaces
            resp = resp.strip()
            if resp != "None":
                filtered_items = filtered_items + json.loads(resp)
        
        # TODO: remove the print statement, this is for debugging and filtering only
        print("[DEBUG MSG] OpenAI found these items:\n", [c for c in contents if c["id"] in filtered_items])
        # save filtered items
        self.save_func(filtered_items)