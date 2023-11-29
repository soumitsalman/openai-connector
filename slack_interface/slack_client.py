import datetime
import config
import social_media_datastore.dataservice as ds
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=config.get_slack_bot_token())

def start():
    SocketModeHandler(app, config.get_slack_app_token()).start()

@app.command("/newitems")
def show_new_posts(ack, respond):
    # pass the kind value as a parameter
    ack()
    _get_items_and_display(ds.ProcessingStage.INTERESTING, "soumitsr@gmail.com", respond)


@app.action("interesting_items_action")
def act_on_interesting_items(ack, payload):
    ack()
    print(payload.get("value"))


def _get_items_and_display(where, who, respond):
    items = [sr for sr in ds.get_contents_for_processing(where, who, max_items=5)]
    respond(blocks=_get_item_displayblock(items_metadata=items))
    
def _get_item_displayblock(items_metadata: [dict]):
    date_str = lambda float_val: datetime.datetime.fromtimestamp(float_val).strftime("%b %d, %Y") 
    post_and_comment_context = lambda data: {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": f":basketball: {data.get('score', 0)}"
            },
            {
                "type": "plain_text",
                "text": f":ok_hand: {data.get('upvote_ratio', 0)*100}%"
            },
            {
                "type": "plain_text",
                "text": f":left_speech_bubble: {data.get('num_comments', 0)}"
            },                               
            {
                "type": "plain_text",
                # TODO: pull-in from data after it is ready
                "text": f":card_index_dividers: {data.get('topic', 'misc.')}"
            },
            {
                "type": "plain_text",
                "text": f":date: {date_str(data.get('created'))}"
            }
        ]
    }
    channel_context = lambda data: {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": f":busts_in_silhouette: {data.get('num_subscribers', 0)}"
            },
            {
                "type": "plain_text",
                "text": f":card_index_dividers: {data.get('topic', 'misc.')}"
            }
        ]
    }
    post_and_comment_section = lambda data: {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"[<{data.get('url')}|r/{data.get('channel')}>] *{data.get('title', '')}*\n{data.get('text')}\n{data.get('summary')}"
		},
		"accessory": {
			"type": "overflow",
			"options": [
				{
					"text": {
						"type": "plain_text",
						"text": ":left_speech_bubble: Comment",
                        "emoji": True
					},
					"value": f"comment {data['id']}"
				},
				{
					"text": {
						"type": "plain_text",
						"text": ":file_folder: Save for later",
                        "emoji": True
					},
					"value": f"save {data['id']}"
				},
				{
					"text": {
						"type": "plain_text",
						"text": ":roll_of_paper: Trash",
                        "emoji": True
					},
					"value": f"trash {data['id']}"
				}
			],
			"action_id": "interesting_items_action"
		}
	}
    channel_section = lambda data: {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"[<{data.get('url')}|r/{data.get('channel')}>] *{data.get('title')}*\n*Summary*: {data.get('summary')}\n*Description*: {data.get('text')}"
		},
		"accessory": {
			"type": "overflow",
			"options": [
				{
					"text": {
						"type": "plain_text",
						"text": ":left_speech_bubble: Subscribe",
                        "emoji": True
					},
					"value": f"subscribe {data['id']}"
				},				
				{
					"text": {
						"type": "plain_text",
						"text": ":roll_of_paper: Trash",
                        "emoji": True
					},
					"value": f"trash {data['id']}"
				}
			],
			"action_id": "interesting_items_action"
		}
	}
    divider = {"type": "divider"}
    blocks = []
    for metadata in items_metadata:
        print(metadata)
        if metadata["kind"] == "subreddit":
            new_set = [
                channel_context(metadata),
                channel_section(metadata),
                divider
            ]
        else:
            new_set = [
                post_and_comment_context(metadata),
                post_and_comment_section(metadata),
                divider
            ]
        blocks = blocks + new_set
    return blocks

