import requests
import os
TOKEN = os.environ['PAGE_ACCESS_TOKEN']
url = 'https://graph.facebook.com/v2.6/me/messenger_profile'
data = {"get_started": {"payload": "getstarted"}}
params = {"access_token": TOKEN}
headers={"Content-Type": "application/json"}
response = requests.post(url, json=data, params=params, headers=headers)
print(response.status_code)
print(response.text)