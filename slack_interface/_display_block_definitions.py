import datetime
import random

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

_system_messages = {
    "error": [
		"Oops, Doggystyle Error! Looks like this feature is straight outta development, my friend. Kick back and stay tuned for some future funk.",
		"Fo' Shizzle, Not Implemented! Hey, homie, we haven't dropped that feature yet. We're cookin' it up in the studio. Keep it chill and check back later.",
		"No D-O-Double-G on This Feature. This feature ain't in the Dogg's house yet. We're smokin' up some code for it. Roll back later, and we'll drop it like it's hot.",
		"Ain't Nothin' but a 'Not Implemented' Thang. It's a G thang, but this feature ain't part of the gang yet. We're layin' down the beats for it. Stay tuned, playa.",
		"Nothin' but 'Not Implemented,' Baby. Ain't no sunshine on this feature today. We're on that grind to make it happen. Keep it real and come back later.",
		"Mi Bredda, We Got a Likkle Error Yah! Dis feature nah ready yet. Hold a vibes and check back latah when we got it all irie.",
		"Rasclaat! Dis Not Implemented, Yuh Know! Mi apologize, but dis ting ain't cooked up yet. Mi team a work pon it. Soon come, mi friend.",
		"No D-O-Double-G inna Dis Feature. Dis one nuh deh a di yard yet. We a simmer and stew di code fi it. Gwan hol' a meditation, and it soon ready.",
		"Ain't Nuttin' but a 'Not Implemented' T'ing. A di Irie vibes, but dis feature nuh part a di link-up yet. We a lay down di riddim fi it. Stay tuned, mi bredren.",
		"Mi Tell Yuh, 'Not Implemented,' Bredda. No sunshine pon dis feature today. Wi deh pon di grind fi mek it happen. Keep it roots, and come back soon, mi seh."
	],
    "wait": [
        "Yo, just chillax while we do our thing and process your request, ya dig?",
		"Hold up, we're layin' down some processing magic for ya, stay groovy...",
		"We in the zone, processing your stuff, so kick back and ride the wave, baby...",
		"We're on it, processing your task, so hang tight, it's all good...",
		"Stay cool, we're handling the operation, just vibin' with it, ya feel me?",
		"Mi beg yuh likkle patience while we process yuh request, ya man?",
		"Hold on deh, we a work pon yuh request right now, stay irie...",
		"Wi deh pon di job, processing yuh ting, so kick back and enjoy di vibes, mi bredda...",
		"Wi deh pan it, processing yuh task, so tek a likkle rest, everyting bless...",
		"Stay cool, we a handle di operation, just a groove to di rhythm, ya understand?",
		"Sit quietly and witness the majestic processing of your request, for I have decreed it!",
		"Hold your horses, for we are in the midst of a majestic procession, and you shall observe in silent awe.",
		"We, the diligent workforce, are fervently engaged in the processing of your matter; remain still and heed the might of our efforts.",
		"We, the loyal servants, are tending to your task. You are commanded to remain at rest while we fulfill our duty.",
		"Behold, as we masterfully oversee the operation. Do not dare disrupt the proceedings, for it is so decreed by Aladeen!"
	],
    "scheduled": [
		"Arr, ye've successfully scheduled yer task, savvy? It be ready and waitin' for yer command!",
		"Hoist the colors! Yer appointment be confirmed and set to sail on the date and time ye requested.",
		"Aye, matey! There be an exciting event on the horizon, and we've scheduled yer task for it. Get ready for some productive plunderin'!",
		"Yer task be in the queue, mate. We've got it on our radar, ready to set sail at a moment's notice.",
		"Ahoy, ye scallywag! Yer plan be set in stone. We've scheduled yer task as requested. Time to mark it off yer to-do list and sail the high seas!",
        "You've scheduled your task, my friend. It's been done. Consider it a favor."
		"Your appointment, it's confirmed. It will happen as requested. A sign of respect.",
		"An event approaches, and your task is part of the plan. We've scheduled it for you, as a gesture of goodwill.",
		"Your task is in the queue, waiting for its turn. We're keeping an eye on it."
		"Your plan is set. Your task is scheduled as you wished. A token of our appreciation."
	],
    "trashed": [
		"Flushed it dung inna di toilet.",
		"Send it weh inna di toilet.",
		"Dropped it inna di toilet and flush.",
		"Put it inna di toilet and give it a flush.",
		"Sank it inna di toilet wid a flush.",
        "Dumped it in the crapper and gave it a good flush.",
		"Sent it down the pipes in the toilet.",
		"Dropped it like a champ in the john and watched it vanish.",
		"Chuck it in the toilet and pull the trigger.",
		"Flushed it down the bowl, no questions asked."
	]
}

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
    
    for metadata in items_metadata:
        if metadata["kind"] == "subreddit":
            new_set = [
                channel_context(metadata),
                channel_section(metadata)
            ]
        else:
            new_set = [
                post_context(metadata),
                post_section(metadata)
            ]
        yield new_set

def get_system_message(event_type):
    return _system_messages[event_type][random.randint(0, len(_system_messages[event_type])-1)]
    
