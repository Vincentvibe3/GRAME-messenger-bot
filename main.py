import requests
import json
import os

TOKEN = os.environ['PAGE_ACCESS_TOKEN']

class response():
    def __init__(self, data):
        self.message = data['message']['text']
        self.user = data['sender']['id']

class registration():
    def __init__(self, data):
        pass

def send_message(message, user_id):
    request = {"recipient":{"id": user_id}, "message": {"text":message}}
    print(request)
    payload = {"access_token": TOKEN}
    url = "https://graph.facebook.com/v9.0/me/messages"
    send = requests.post(url, params=payload, json=request)