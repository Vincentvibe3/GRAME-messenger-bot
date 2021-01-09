import requests
import json
import os

memberslist = open('members.json', 'w')

TOKEN = os.environ['PAGE_ACCESS_TOKEN']

{'sender': {'id': '3824615787560191'}, 'recipient': {'id': '100437728693507'}, 'timestamp': 1610204414942, 'postback': {'title': 'postback Button', 'payload': 'test'}}

class response():
    def __init__(self, data):
        self.user = data['sender']['id']
        self.data = data
    
    def set_message(self):
        if 'postback' in self.data:
            self.message = self.data['postback']['title']
            self.payload = self.data['postback']['payload']
            self.type = 'postback'
        else:
            self.message = self.data['message']['text']
            self.type = 'message'

class registration():
    def __init__(self, data):
        pass

def check_scenario(response):
    if response.type == 'postback':
        if response.payload == 'getstarted':
            message = 'Would you like to register?'
            user = response.user
            choices = [{"type":"postback", "title":"Yes", "payload":"Register"}, {"type":"postback", "title":"No", "payload":"No Register"}]
            send_message(message, user, choices)
        else:
            send_message('hello', response.user)
    else:
        send_message('message', response.user)
    

def check_membership():
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

def get_password():
    with open('Password.txt', 'r') as secret_file:
        password = secret_file.read()
    return password

def send_email(name, email, phone_number, availibilities):
    subject = "Registration: " + name
    body = 'Name: ' + name + '\nE-mail: ' + email + '\nPhone Number: ' + phone_number + '\nAvailabilities: ' + availibilities + " hours per week"
    sender_email = 'messenger.bot.logs@gmail.com'
    receiver_email = 'keveleven26@gmail.com'
    password = get_password()
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

