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
#main file
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(name, email, phone_number, availibilities):
    subject = "Registration: " + name
    body = 'Name: ' + name + '\nE-mail: ' + email + '\n Phone Number: ' 
    + phone_number + '\n Availabilities: ' + availibilities


