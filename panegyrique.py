from flask import Flask, request, make_response
from slack import WebClient
import json
import os

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# This `app` represents your existing Flask app
app = Flask(__name__)

# An example of one of your Flask app's routes
@app.route("/")
def hello():
  return "Hello there!"


slack_client = WebClient(SLACK_BOT_TOKEN)

receiver_user_id = None

# Shortcut (salck action)
@app.route("/slack/action", methods=['POST'])
def slack_action():
    global receiver_user_id
    d = request.form.to_dict()
    payload = json.loads(d['payload'])

    if payload['type'] == 'shortcut':
        trigger_id = payload['trigger_id']
        view = """{
    	"title": {
    		"type": "plain_text",
    		"text": "Féliciter quelqu'un"
    	},
    	"submit": {
    		"type": "plain_text",
    		"text": "Envoyer"
    	},
    	"blocks": [
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "Sélectionner la personne qui recevra le message"
    			},
    			"accessory": {
    				"type": "users_select",
    				"placeholder": {
    					"type": "plain_text",
    					"text": "Select a user",
    					"emoji": true
    				}
    			}
    		},
    		{
    			"type": "input",
    			"element": {
    				"type": "plain_text_input",
    				"multiline": true
    			},
    			"label": {
    				"type": "plain_text",
    				"text": "Message",
    				"emoji": true
    			}
    		}
    	],
    	"type": "modal"
        }"""


        slack_client.views_open(
            trigger_id=trigger_id,
            view=view
        )

    elif payload['type'] == 'block_actions':
        receiver_user_id = payload['actions'][0]['selected_user']

    elif payload['type'] == 'view_submission':
        user_id = payload['user']['id']
        block_id = payload['view']['blocks'][1]['block_id']
        action_id = payload['view']['blocks'][1]['element']['action_id']
        message = "Quelqu'un t'a envoyé un message :tada:\n"
        message += payload['view']['state']['values'][block_id][action_id]['value']
        slack_client.chat_postMessage(
            channel=receiver_user_id,
            text=message
        )

    return make_response("", 200)


# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=3000)
