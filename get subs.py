import requests
import os
TOKEN = os.environ['PAGE_ACCESS_TOKEN']
id = '100437728693507'
url = 'https://graph.facebook.com/v9.0/100437728693507/subscribed_apps?access_token=%s'%(TOKEN)
data = {"get_started": {"payload": "getstarted"}}
params = {"access_token": TOKEN}
headers={"Content-Type": "application/json"}
response = requests.get(url)#, json=data, params=params, headers=headers)
print(response.url)
print(response.status_code)
print(response.text)