from flask import Flask, request, redirect, abort
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    print('test')
    return 'Welcome'

@app.route('/webhook', methods=['POST'])
def post_to_webhook():
    body = request.get_json()
    if body['object']=='page':
        for entry in body['entry']:
            webhook_event = entry['messaging'][0]
        return 'EVENT_RECEIVED'
    else:
        abort(404) 



@app.route('/webhook', methods=['GET'])
def webhook():
    TOKEN = os.environ['PAGE_ACCESS_TOKEN']
    try:
        mode = request.args.get('hub.mode', None)
        token = request.args.get('hub.verify_token', None)
        challenge = request.args.get('hub.challenge', None)
    except:
        abort(403)
    
    print((mode, token, challenge))
    if mode == 'subscribe' and token == TOKEN:
        return challenge
    else:
        abort(404)