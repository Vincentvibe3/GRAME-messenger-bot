from flask import Flask, request, redirect, abort
import os
import main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    '''index (not used)'''
    return 'Welcome'

@app.route('/check-events', methods=['GET'])
def check():
    '''Endpoint to call to check for a new event'''
    #get new events
    new_events = main.get_new_events()
    #check for new events
    if new_events:
        #send message on new event
        main.new_event_message()
    #respond with 'OK'
    return 'OK'

@app.route('/webhook', methods=['POST'])
def post_to_webhook():
    '''Endpoint where facebook posts on a message sent by user'''
    #get request body in json format
    body = request.get_json()
    #check if the response comes from a page
    if body['object']=='page':
        #checks all entries delivered
        for entry in body['entry']:
            #sets webhook_event as the message
            webhook_event = entry['messaging'][0]
        #create a response object for webhook_event(see main.py for response class)
        message_response = main.response(webhook_event)
        #set the content of message
        message_response.set_message()
        #check for action to be done
        main.check_scenario(message_response)
        #respond to facebook
        return 'EVENT_RECEIVED'
    else:
        #respond with 404
        abort(404) 



@app.route('/webhook', methods=['GET'])
def webhook():
    '''Endpoint to authorize webhook'''
    #webhook set in facebook dev console
    WEBHOOK_TOKEN = os.environ['WEBHOOK_ACCESS_TOKEN']
    #try to set mode, token, challenge from GET parameters
    try:
        mode = request.args.get('hub.mode', None)
        token = request.args.get('hub.verify_token', None)
        challenge = request.args.get('hub.challenge', None)
    except Exception:
        #on error respond with 403
        abort(403)
    
    #authentification
    if mode == 'subscribe' and token == WEBHOOK_TOKEN:
        return challenge
    else:
        #send 404 code
        abort(404)