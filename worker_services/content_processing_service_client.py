import json
import config
from openai_interface.basicclient import BasicClient

# service client
class ContentProcessingServiceClient:
    # TODO: check is user_id even needed
    def __init__(self, instructions, prompt, collect_func, save_func, process_name = None):
        self.name = process_name
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
        # TODO: remove this - debug purpose only
        print(f"[DEBUG MSG] {len(contents)} items collected by {self.name}")

        filtered_items = []
        #process each item as they come back
        for resp in self.client.send_batch(msgs = [json.dumps(c) for c in contents], prompt = self.prompt):
            #remove the leading and trailing whitespaces
            resp = resp.strip()
            if resp != "None":
                try:
                    filtered_items = filtered_items + json.loads(resp)
                except:
                    print(f"{self.name} could not parse {resp}")
        
        # TODO: remove the print statement, this is for debugging and filtering only
        # print("[DEBUG MSG] OpenAI found these items:\n", filtered_items)
        # save filtered items
        self.save_func(filtered_items)
        # TODO: remove this - debug purpose only
        print(f"[DEBUG MSG] {len(filtered_items)} items saved by {self.name}")