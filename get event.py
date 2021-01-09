import requests
import os
TOKEN = os.environ['PAGE_ACCESS_TOKEN']
params = {"access_token": TOKEN}
id = '415948276274773'
url = 'https://graph.facebook.com/v9.0/%s'%(id)
response = requests.get(url, params=params)
print(response.url)
print(response.status_code)
print(response.text)