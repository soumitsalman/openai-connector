import datetime
import json
import re
import config
import social_media_datastore.dataservice as ds
import slack_interface._display_block_definitions as blocks
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

"""
LESSONS LEARNED:
Essentially what matters to me is "app.message" app.action and app.command
For app.message the message parameter matters
For app.action the payload/action parameter matters. payload and action are same here
    I should assign a blockID = id of the content because that is unique identifier
    Value shows what the actions is (save, comment, subscribe, trash)
    I can use say or respond for sending what I want
For app.command make sure that I dont have too many commands
    I can simply handle them as functions
message and body has user id information
respond will only respond to the person that initiated it. The original message will disappear once I respond
Say will share this everyone and the original message will not disappear
"""

app = App(token=config.get_slack_bot_token())

def start():
    SocketModeHandler(app, config.get_slack_app_token()).start()

@app.command("/newitems")
def show_new_posts(ack, say, command):
    # pass the kind value as a parameter
    ack()
    if command['user_id'] != "U0G95QKJ6":
        say(f"Well ... you ain't <@U0G95QKJ6> but i'll show you his shit anyway, cause fuck em!")
    else:
        say("Here is a list of top selection")
    _get_items_and_display(ds.ProcessingStage.INTERESTING, "soumitsr@gmail.com", say)

@app.action("item_action_start")
def start_user_action(ack, action, body, say):
    ack()
    say(f"<@{body['user']['id']}> wants to {action['selected_option']['value']} to {action['block_id']}")

def _get_items_and_display(where, who, say):
    items = [sr for sr in ds.get_contents_for_processing(where, who, max_items=5)]
    say(blocks=blocks.get_items_displayblocks(items_metadata=items))

@app.message("buttons")
def _TEST_show_buttons(say, message):

    say(text = "showing a butt load of buttons", blocks=blocks._TEST_get_random_buttons())
    print(json.dumps([message]), ",\n")


@app.action(re.compile("(actionId-0|button-action|overflow-action|static_select-action|users_select-action)"))
def _TEST_random_action_function(ack, payload, action, body, message, say):
    ack()
    say("Wah gwaan man!")    
    print(json.dumps([payload, action, body]),",\n")
    




    

