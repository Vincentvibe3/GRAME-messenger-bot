from flask import Flask, request, redirect, abort
import os
import main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome'

@app.route('/check-events', methods=['GET'])
def check():
    new_events = main.get_new_events()
    if new_events:
        main.new_event_message()
    return 'OK'

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
        #buttons = [{"type":"postback", "title":"postback Button", "payload":"test"}, {"type":"postback", "title":"hello", "payload":"test"}]
        #main.send_message('hello world', message_response.user)#, buttons)
        return 'EVENT_RECEIVED'
    else:
        abort(404) 



@app.route('/webhook', methods=['GET'])
def webhook():
    WEVHOOK_TOKEN = os.environ['WEBHOOK_ACCESS_TOKEN']
    try:
        mode = request.args.get('hub.mode', None)
        token = request.args.get('hub.verify_token', None)
        challenge = request.args.get('hub.challenge', None)
    except:
        abort(403)
    
    if mode == 'subscribe' and token == WEBHOOK_TOKEN:
        return challenge
    else:
        abort(404)