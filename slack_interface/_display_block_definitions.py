import datetime

def _TEST_get_random_buttons():
    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Test block with users select"
			},
			"accessory": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a user",
					"emoji": True
				},
				"action_id": "users_select-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick an item from the dropdown list"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					}
				],
				"action_id": "static_select-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "This is a section block with a button."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Click Me 1",
					"emoji": True
				},
				"value": "click_me_1VAL",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "This is a section block with a button."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Click Me 2",
					"emoji": True
				},
				"value": "click_me_2VAL",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "This is a section block with an overflow menu."
			},
			"accessory": {
				"type": "overflow",
				"options": [					
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-3"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-4"
					}
				],
				"action_id": "overflow-action"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Click Me",
						"emoji": True
					},
					"value": "click_me_random button",
					"action_id": "actionId-0"
				}
			]
		}
	]

def get_items_displayblocks(items_metadata: [dict]):
    date_str = lambda float_val: datetime.datetime.fromtimestamp(float_val).strftime("%b %d, %Y") 
    post_context = lambda data: {
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
    post_section = lambda data: {
        "block_id": data['id'],
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
					"value": "comment"
				},
				{
					"text": {
						"type": "plain_text",
						"text": ":roll_of_paper: Trash",
                        "emoji": True
					},
					"value": "trash"
				}
			],
			"action_id": "item_action_start"
		}
	}
    channel_section = lambda data: {
        "block_id": data['id'],
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": f"[<{data.get('url')}|r/{data.get('channel')}>] *{data.get('title')}*\n*Summary*: {data.get('summary')}"
		},
		"accessory": {
			"type": "overflow",
			"options": [
				{
					"text": {
						"type": "plain_text",
						"text": ":handshake: Subscribe",
                        "emoji": True
					},
					"value": "sub"
				},				
				{
					"text": {
						"type": "plain_text",
						"text": ":roll_of_paper: Trash",
                        "emoji": True
					},
					"value": "trash"
				}
			],
			"action_id": "item_action_start"
		}
	}
    divider = {"type": "divider"}
    blocks = []
    for metadata in items_metadata:
        if metadata["kind"] == "subreddit":
            new_set = [
                channel_context(metadata),
                channel_section(metadata),
                divider
            ]
        else:
            new_set = [
                post_context(metadata),
                post_section(metadata),
                divider
            ]
        blocks = blocks + new_set
    return blocks
