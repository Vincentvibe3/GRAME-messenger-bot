from flask import Flask, request, redirect, abort
import os
import main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome'

@app.route('/webhook', methods=['POST'])
def post_to_webhook():
    body = request.get_json()
    if body['object']=='page':
        for entry in body['entry']:
            webhook_event = entry['messaging'][0]
        print(webhook_event)
        message_response = main.response(webhook_event)
        message_response.set_message()
        main.check_scenario(message_response)
        return 'EVENT_RECEIVED'
    else:
        abort(404) 



@app.route('/webhook', methods=['GET'])
def webhook():
    TOKEN = os.environ['WEBHOOK_ACCESS_TOKEN']
    try:
        mode = request.args.get('hub.mode', None)
        token = request.args.get('hub.verify_token', None)
        challenge = request.args.get('hub.challenge', None)
    except:
        abort(403)
    
    if mode == 'subscribe' and token == TOKEN:
        return challenge
    else:
        abort(404)