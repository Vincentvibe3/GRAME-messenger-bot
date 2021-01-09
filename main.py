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
            self.payload = self.data['postback']['payload']
            self.type = 'postback'
        else:
            self.message = self.data['message']['text']
            self.type = 'message'

class registration():
    def __init__(self, data):
        pass

def set_user_state(user, state):
    memberslist = open('members.json', 'r')
    try:
        members = json.loads(memberslist.read())
    except Exception:
        members = {}
    memberslist.close()
    try:
        members[user]['state'] = state
    except Exception:
        members[user] = {}
        members[user]['state'] = state
    memberslist = open('members.json', 'w')
    memberslist.write(json.dumps(members, indent=4))
    memberslist.close()
    
def get_user_state(user):
    memberslist = open('members.json', 'r')
    members = json.loads(memberslist.read())
    memberslist.close()
    state = members[user]['state']
    return state

def get_started(user):
    message = 'Would you like to register?'
    choices = [{"type":"postback", "title":"Yes", "payload":"Register"}, {"type":"postback", "title":"No", "payload":"No Register"}]
    send_message(message, user, choices)

def ask_question(message, user, nextstate):
    send_message(message, user)
    set_user_state(user, nextstate)

def get_info(user, state, response):
    info = response.message
    write_user_info(user, state, info)

def write_user_info(user, info, value):
    memberslist = open('members.json', 'r')
    members = json.loads(memberslist.read())
    memberslist.close()
    members[user][info] = value
    memberslist = open('members.json', 'w')
    memberslist.write(json.dumps(members, indent=4))
    memberslist.close()


def check_scenario(response):
    states = [{'name':'name', 'message':'What is your name? (ex: Smith, John)'}, {'name':'email', 'message': 'What is your E-mail address? (ex: John.Smith@gmail.com)'}, 
    {'name':'phone_number', 'message':'What is your phone number? (ex: 438-675-8956)'}, {'name':'availibilities', 'message':'How many hours are you available a week? (ex: 5)'},
    {'name':'Registered', 'message':'Thank you for helping!'}]
    user = response.user
    if response.type == 'postback':
        if response.payload == 'getstarted':
            get_started(user)
        elif response.payload == "No Register":
            send_message('Thank you for your time', user)
        elif response.payload == "Register":
            ask_question(states[0]['message'], user, 'name')

    else:
        user_state = get_user_state(user)
        if user_state != 'Registered':
            for state in states:
                print('checking states')
                if user_state == state['name']:
                    current_index = states.index(state)
                    print(current_index)
                    get_info(user, state['name'], response)
                    ask_question(states[current_index+1]['message'], user, states[current_index+1]['name'])
    

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

