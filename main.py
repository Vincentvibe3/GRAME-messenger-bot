"""This program requires the following dependencies"""
import requests
import json
import os
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Token to access a page
TOKEN = os.environ['PAGE_ACCESS_TOKEN']

class response():
    """represents a message received from facebook
        It sets the information needed to send back messages"""
    def __init__(self, data):
        #get the message's sender
        self.user = data['sender']['id']
        #sets the received data for future use in set_message
        self.data = data
    
    def set_message(self):
        """Checks for the messaging time and sets information accordingly"""
        if 'postback' in self.data:
            #sets message
            self.message = self.data['postback']['title']
            #sets received payload
            self.payload = self.data['postback']['payload']
            #sets the message type
            self.type = 'postback'
        else:
            #sets message
            self.message = self.data['message']['text']
            #sets message type
            self.type = 'message'


def set_user_state(user, state):
    """Sets the state where the user is at in a scenario
        requires a user and the state to set"""
    #opens the file where users who accepted registration are stored
    memberslist = open('members.json', 'r')
    #try to load the content as json
    #failure on an empty file
    try:
        members = json.loads(memberslist.read())
    #Exception to be specified
    except Exception:
        #on an empty file create an empty dictionary
        members = {}
    #close file
    memberslist.close()
    try:
        #tries to set state
        members[user]['state'] = state
    #Exception to be specified
    except Exception:
        #if user is not present create user
        members[user] = {}
        #set user state
        members[user]['state'] = state
    
    #open file storing users for writing
    memberslist = open('members.json', 'w')
    #write all users to the file
    memberslist.write(json.dumps(members, indent=4))
    #close file
    memberslist.close()
    
def get_user_state(user):
    """gets the state for a certain user
        requires the user to get"""
    #open list of users for reading
    memberslist = open('members.json', 'r')
    #try to load as json
    try:
        members = json.loads(memberslist.read())
    #Exception to be specified
    except Exception:
        #on failure return state as 'No entry'
        state = 'No entry'
    else:
        #set state variable to the users state
        state = members[user]['state']
    #close file
    memberslist.close()
    #return the uses state
    return state

def get_started(user):
    """Called when a user presses on the get started event
        Sends a message in response to the get started event
        requires the user who pressed on the button"""
    #set message to send
    message = 'Would you like to register?'
    #set the buttons for choices
    choices = [{"type":"postback", "title":"Yes", "payload":"Register"}, {"type":"postback", "title":"No", "payload":"No Register"}]
    #send the message in response to the get started event
    send_message(message, user, choices)

def ask_event(user):
    '''Send a message asking if a user wants to participate in an event
        requires: user to send the message to'''
    #message
    message = 'Would you be interested in participating in this event? (say yes for more details)'
    #buttons
    choices = [{"type":"postback", "title":"Yes", "payload":"Participate"}, {"type":"postback", "title":"No", "payload":"No Participate"}]
    #send message
    send_message(message, user, choices)

def ask_for_confirmation(user):
    '''ask user for confirmation for their participation'''
    #message
    message = 'Confirm your participation'
    #buttons
    choices = [{"type":"postback", "title":"Yes", "payload":"Confirmed"}, {"type":"postback", "title":"Cancel", "payload":"Canceled"}]
    #send message
    send_message(message, user, choices)   

def ask_question(message, user, nextstate):
    """asks the user a question
        sends the question and changes the user state to check for a different response than previously
        requires the message to send, the user to send to, and the state to change to"""
    #sends the text
    send_message(message, user)
    #changes the user state to the nextstate needed
    set_user_state(user, nextstate)

def get_info(user, state, response):
    '''Stores the information a user supplies in a message,
        the information is in response to a certain state in a scenario
        and will be associated with that state
        requires the user that replied, the message response received and the state to associate to'''
    #sets the info received (message content)
    info = response.message
    #writes the info to a file
    write_user_info(user, state, info)

def write_user_info(user, info, value):
    '''Writes info from a user to a file
        requires the user to write to, the information type and its value'''
    #opens file for reading
    memberslist = open('members.json', 'r')
    #loads the users
    members = json.loads(memberslist.read())
    #closes the file
    memberslist.close()
    #sets the user info
    members[user][info] = value
    #open file for writing
    memberslist = open('members.json', 'w')
    #write all users
    memberslist.write(json.dumps(members, indent=4))
    #close file
    memberslist.close()

def get_name(user):
    memberslist = open('members.json', 'r')
    members = json.loads(memberslist.read())
    memberslist.close()
    name = members[user]['name']
    return name

def get_all_info(user):
    '''get all the information supplied by a user
        requires the user'''
    #to rewrite
    memberslist = open('members.json', 'r')
    members = json.loads(memberslist.read())
    memberslist.close()
    name = members[user]['name']
    email = members[user]['email']
    phone_number = members[user]['phone_number']
    availibilities = members[user]['availibilities']
    return name, email, phone_number, availibilities

def check_scenario(response):
    '''Check for action to do in response to a message
        requires: object from response class response'''
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

def get_new_events():
    '''gets new events for the page'''
    #to rewrite removing hardcoded elements
    new_events = []
    allevents = []
    logged_events_file = open('events.json', 'r')
    try:
        logged_events = json.loads(logged_events_file.read())
    #Exception to be specified
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
        event_id = event['id']
        if event_id not in logged_events:
            new_events.append(event)
            logged_events.append(event_id)
        allevents.append(event_id)
    
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
    '''Send all users registered a message on a new event'''
    #open user list for reading
    users_file = open('members.json', 'r')
    #get users
    users = json.loads(users_file.read())
    #send message for all users
    for user in users:
        #send message notifying
        send_message('There will be an upcoming event.', user)
        #send message asking if you want more info
        ask_event(user)


def send_message(message, user_id, buttons=[]):
    '''Send a message to a specific user
        requires the message content, the user to send to
        optional: buttons that a user can press'''
    #check if CTA(call to action) buttons are given
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
    
    #sets the request parameters
    params = {"access_token": TOKEN}
    #set the url of the targeted endpoint
    url = "https://graph.facebook.com/v9.0/me/messages"
    #send the message
    requests.post(url, params=params, json=request)

def get_password():
    with open('Password.txt', 'r') as secret_file:
        password = secret_file.read()
    return password

def form_register_email(name, email, phone_number, availibilities):
    '''format an email for registration
    note: to be rewritten as function for all scenarios'''
    subject = "Registration: " + name
    body = 'Name: ' + name + '\nE-mail: ' + email + '\nPhone Number: ' + phone_number + '\nAvailabilities: ' + availibilities + " hours per week"
    return subject, body

def form_confirmed_participation_email(name, event_name):
    '''see form_register_email()'''
    subject = name + " is participating!"
    body = name + " has confirmed his participation to" + event_name + "."
    return subject, body

def send_email(subject, body):
    '''send an email on behalf of an email account
        requires the subject and the body of the email'''
    #set the sender of the email
    sender_email = 'messenger.bot.logs@gmail.com'
    #set the receiver of the email(to be moved to arguments)
    receiver_email = 'keveleven26@gmail.com'
    #get password of sender
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