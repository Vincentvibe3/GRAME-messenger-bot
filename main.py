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
    try:
        members = json.loads(memberslist.read())
    except Exception:
        state = 'No entry'
    else:
        state = members[user]['state']
    memberslist.close()
    return state

def get_started(user):
    message = 'Would you like to register?'
    choices = [{"type":"postback", "title":"Yes", "payload":"Register"}, {"type":"postback", "title":"No", "payload":"No Register"}]
    send_message(message, user, choices)

def ask_event(user):
    message = 'Would you be interested in participating in this event? (say yes for more details)'
    choices = [{"type":"postback", "title":"Yes", "payload":"Participate"}, {"type":"postback", "title":"No", "payload":"No Participate"}]
    send_message(message, user, choices)

def ask_for_confirmation(user):
    message = 'Confirm your participation'
    choices = [{"type":"postback", "title":"Yes", "payload":"Confirmed"}, {"type":"postback", "title":"Cancel", "payload":"Canceled"}]
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

def get_name(user):
    memberslist = open('members.json', 'r')
    members = json.loads(memberslist.read())
    memberslist.close()
    name = members[user]['name']
    return name

def get_all_info(user):
    memberslist = open('members.json', 'r')
    members = json.loads(memberslist.read())
    memberslist.close()
    name = members[user]['name']
    email = members[user]['email']
    phone_number = members[user]['phone_number']
    availibilities = members[user]['availibilities']
    return name, email, phone_number, availibilities

def check_scenario(response):
    user = response.user
    user_state = get_user_state(user)
    if user_state != 'Registered':
        #registration
        states = [{'name':'name', 'message':'What is your name? (ex: Smith, John)'}, {'name':'email', 'message': 'What is your E-mail address? (ex: John.Smith@gmail.com)'}, 
        {'name':'phone_number', 'message':'What is your phone number? (ex: 438-675-8956)'}, {'name':'availibilities', 'message':'How many hours are you available a week? (ex: 5)'},
        {'name':'Registered', 'message':'Thank you for helping!'}]
        if response.type == 'postback':
            if response.payload == 'getstarted':
                get_started(user)
            elif response.payload == "No Register":
                send_message('Thank you for your time', user)
            elif response.payload == "Register":
                ask_question(states[0]['message'], user, 'name')

        else:
            for state in states:
                print('checking states')
                if user_state == state['name']:
                    current_index = states.index(state)
                    print(current_index)
                    get_info(user, state['name'], response)
                    ask_question(states[current_index+1]['message'], user, states[current_index+1]['name'])
                    if state['name'] == states[-2]['name']:
                        name, email, phone_number, availibilities = get_all_info(user)
                        subject, body = form_register_email(name, email, phone_number, availibilities)
                        send_email(subject, body)
    else:
        #other actions
        new_events_file = open('new_events.json', 'r')
        new_events = json.loads(new_events_file.read())
        location = new_events[0]['place']['location']['city']
        date = new_events[0]['start_time']
        description = new_events[0]['description']
        event_name = new_events[0]['name']
        # event_confirmation(user, response)
        if response.type == 'postback':
            if response.payload == 'Participate':
                send_message(event_name, user)
                send_message('The event will take place in ' + location, user)
                send_message('Date: ' + date, user)
                send_message('Event description: ' + description, user)
                ask_for_confirmation(user)
            elif response.payload == 'Confirmed':
                send_message('Thank you for participating!', user)
                name = get_name(user)
                subject, body = form_confirmed_participation_email(name, event_name)
                send_email(subject, body)

            elif response.payload == 'Canceled':
                send_message('Understandable, have a nice day.', user)
            elif response.payload == 'No Participate':
                send_message('No problem. See you next time!', user)

# def event_confirmation(user, response, event):
#     if response.type == 'postback':
#                 if response.payload == 'Participate':
#                     send_message(event_name, user)
#                     send_message('The event will take place in ' + location, user)
#                     send_message('Date: ' + date, user)
#                     send_message('Event description: ' + description, user)
#                     if response.type == 'postback':
#                         if response.payload == 'Confirmed':
#                             send_message('Thank you for participating!', user)
#                             name = get_name(user)
#                             subject, body = form_confirmed_participation_email(name, event_name)
#                             send_email(subject, body)

#                         elif response.payload == 'Canceled':
#                             send_message('Understandable, have a nice day.', user)
#                 elif response.payload == 'No Participate':
#                     send_message('No problem. See you next time!', user)

def get_new_events():
    new_events = []
    allevents = []
    logged_events_file = open('events.json', 'r')
    try:
        logged_events = json.loads(logged_events_file.read())
    except Exception:
        logged_events = []
    logged_events_file.close()
    page_id = '100437728693507'
    params = {"access_token": TOKEN}
    url = 'https://graph.facebook.com/v9.0/%s/events' %(page_id)
    response = requests.get(url, params=params)
    data_json = json.loads(response.text)
    events = data_json['data']
    for event in events:
        id = event['id']
        if id not in logged_events:
            new_events.append(event)
            logged_events.append(id)
        allevents.append(id)
    
    for logged_event in logged_events:
        for event in events:
            if logged_event not in allevents:
                del logged_events[logged_event]

    output_file = open('events.json', 'w')
    output_file.write(json.dumps(logged_events))
    output_file.close()
    print(new_events)
    new_events_file = open('new_events.json', 'w')
    new_events_file.write(json.dumps(new_events))
    new_events_file.close()
    return new_events

def new_event_message():
    users_file = open('members.json', 'r')
    users = json.loads(users_file.read())
    for user in users:
        print(user)
        send_message('There will be an upcoming event.', user)
        ask_event(user)


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


import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_password():
    with open('Password.txt', 'r') as secret_file:
        password = secret_file.read()
    return password

def form_register_email(name, email, phone_number, availibilities):
    subject = "Registration: " + name
    body = 'Name: ' + name + '\nE-mail: ' + email + '\nPhone Number: ' + phone_number + '\nAvailabilities: ' + availibilities + " hours per week"
    return subject, body

def form_confirmed_participation_email(name, event_name):
    subject = name + " is participating!"
    body = name + " has confirmed his participation to" + event_name + "."
    return subject, body

def send_email(subject, body):
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