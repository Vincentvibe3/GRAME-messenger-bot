import requests
import json
import time
import os
import requests
check_url = 'https://43498545725d.ngrok.io/check-events'
next_check = time.time()+1
while True:
    if time.time > next_check:
        requests.get(check_url)
        next_check = time.time()+3600
