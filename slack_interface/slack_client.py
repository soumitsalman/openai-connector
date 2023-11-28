import config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=config.get_slack_bot_token())

def start():
    SocketModeHandler(app, config.get_slack_app_token()).start()

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    sample = """:fire: 97 :thumbsup: 0.93 :speech_balloon: 110
*[r/webdev]*: webdev: reddit for web developers [www.reddit.com/r/t5_2qs0q](https://www.reddit.com/r/t5_2qs0q)
*Text*: A community dedicated to all things web development: both front-end and back-end. For more design-related questions, try /r/web_design. (Cropped to 50 words or less)
*Topic*: Web Development
*User Message*:%s""" % message["text"]

    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": sample}
            }
        ],
        text = sample
    )
    