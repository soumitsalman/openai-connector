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
def show_new_items(ack, respond, command):
    # pass the kind value as a parameter
    ack()
    user_id = ds._get_user_id(command['user_id'])
    _get_items_and_display(from_where=ds.ProcessingStage.INTERESTING, for_who=user_id, to_where=respond)

@app.action("item_action_start")
def start_user_action(ack, action, body, respond):
    ack()
    user_id = ds._get_user_id(body['user']['id'])
    media_action = action['selected_option']['value']
    content_id = action['block_id']
    if media_action == "trash":
       respond(f"{blocks.get_system_message('trashed')} [<@{body['user']['id']}>: {action['selected_option']['value']} --> {action['block_id']}]") 
    elif media_action == "sub":
        ds.que_user_action(
            {
                "user_id": user_id, 
                # TODO: change this to later
                "source": ds.ContentSource.REDDIT.value, 
                "content_id": content_id,
                "action": media_action
            }
        )
        respond(f"{blocks.get_system_message('scheduled')} [<@{body['user']['id']}>: {action['selected_option']['value']} --> {action['block_id']}]")
    else:
        respond(f"{blocks.get_system_message('error')} [<@{body['user']['id']}>: {action['selected_option']['value']} --> {action['block_id']}]")

def _get_items_and_display(from_where, for_who, to_where):
    # change the max_items configuration
    items = [sr for sr in ds.get_contents_for_processing(from_where, for_who, max_items=config.get_max_slack_items_to_show())]
    to_where(f"Here are the top {len(items)} items in the list")
    [to_where(blocks=blocks) for blocks in blocks.get_items_displayblocks(items_metadata=items)]

#@app.message("TEST buttons")
def _TEST_show_buttons(say, message):

    say(text = "showing a butt load of buttons", blocks=blocks._TEST_get_random_buttons())
    print(json.dumps([message]), ",\n")


@app.action(re.compile("(actionId-0|button-action|overflow-action|static_select-action|users_select-action)"))
def _TEST_random_action_function(ack, payload, action, body, message, say):
    ack()
    say("Wah gwaan man!")    
    print(json.dumps([payload, action, body]),",\n")


    




    

