import requests
import json
import os

TOKEN = os.environ['PAGE_ACCESS_TOKEN']

{'sender': {'id': '3824615787560191'}, 'recipient': {'id': '100437728693507'}, 'timestamp': 1610204414942, 'postback': {'title': 'postback Button', 'payload': 'test'}}

class response():
    def __init__(self, data):
        self.user = data['sender']['id']
        self.data = data
    
    def set_message(self):
        if 'postback' in self.data:
            self.message = self.data['postback']['title']
        else:
            self.message = self.data['message']['text']

class registration():
    def __init__(self, data):
        pass


def send_message(message, user_id, buttons=[]):
    #check if CTA buttons are given
    if buttons:
        #creates a message with the supplied list of buttons
        request = {"recipient":{"id": user_id}, 
                "message": {
                    "attachment": {
                        "type": "template", 
                        "payload":{
                            "template_type":"button", 
                            "text": message, 
                            "buttons": buttons
                                }
                            }
                        }
                    }
    else:
        #creates a simple text message
        request = {"recipient":{"id": user_id}, "message": {"text":message}}
    
    payload = {"access_token": TOKEN}
    url = "https://graph.facebook.com/v9.0/me/messages"
    send = requests.post(url, params=payload, json=request)

# def checkresponse(message):
#     if message

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(name, email, phone_number, availibilities):
    subject = "Registration: " + name
    body = 'Name: ' + name + '\nE-mail: ' + email + '\n Phone Number: ' 
    + phone_number + '\n Availabilities: ' + availibilities


