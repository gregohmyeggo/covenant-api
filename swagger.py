from datetime import date, timedelta
import requests, base64, json, datetime, time

# FOR TESTING ONLY; a valid TLS certificate should be used.
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# MAKE SURE TO CHANGE
# <ip>
# <user>
# <password>

url = 'https://<ip>:7443/api'

# Swagger UI Authorization
def getToken():
    headers = { "Content-Type" : "application/json-patch+json" }
    data = { "userName": "<user>", "password": "<password>" }

    r = requests.post(f'{url}/users/login', headers=headers, data=json.dumps(data), verify=False)
    token = r.json()['covenantToken']
    return token

COVENANT_TOKEN = getToken()

headers = { "Authorization" : f"Bearer {COVENANT_TOKEN}",
            "Content-Type" : "application/json" }

#--------------------------------------------------------------------------
def returnGrunt(name):
    grunt = requests.get(f"{url}/grunts/{name}", headers=headers, verify=False)
    return grunt.json()['id']

def interact(name, task):
    grunt_id = returnGrunt(name)
    payload = f"\"{task}\""
    
    output = requests.post(f'{url}/grunts/{grunt_id}/interact', headers=headers, data=payload, verify=False)
    return output.json()

def getGrunts():   
    grunts = requests.get(f"{url}/grunts", headers=headers, verify=False)
    return grunts.json()
#--------------------------------------------------------------------------

completed = []
while True:
    grunts = getGrunts()

    for grunt in grunts:

        # Only returns Grunt information for defined datetime
        if grunt['activationTime'] > str(datetime.date.today()):
            if grunt['status'] == 'active':
                if grunt['integrity'] in ["high", "system"]:
                    if not grunt['name'] in completed:
                        print(f"New SAM entry for {grunt['name']}")
                        
                        # Task Grunt with SamDump
                        interact(grunt['name'], 'SamDump')
                        
                        # Append to completed to prevent duplicate tasks.
                        completed.append(grunt['name'])
    
    time.sleep(60)
