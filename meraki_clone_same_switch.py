
import requests
import json

# User Edit Paramter
organisationname = 'Enter Organisation Name here'
networkname = 'Enter Network Name here'
api_key = 'Enter API Key here'
seriallist = "Enter Serial One here", "Enter Serial Two here"


####### Basic Parameter #######
base_url = 'https://api.meraki.com/api/v0'
headers = {'Accept': '*/*', 'Content-Type': 'application/json','X-Cisco-Meraki-API-Key': '' + api_key + ''}


# Function to remove null value
def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean



# Get Organisation Information
RESOURCE = '/organizations/'
call_response = requests.request("GET", base_url + RESOURCE, headers=headers, data={})
organisation = json.loads(call_response.content)
print('Read all Organisations ' + str(call_response.status_code))
print('###########')

# Fine the Organisation ID
for organisationsearch in organisation:
    x = organisationsearch['name']
    if x == organisationname:
        organisationid = (organisationsearch['id'])


# Get Organisation Information
RESOURCE = '/organizations/' + organisationid + '/networks'
call_response = requests.request("GET", base_url + RESOURCE, headers=headers, data={})
network = json.loads(call_response.content)
print('Read all Networks ' + str(call_response.status_code))
print('###########')

# Fine the Network ID
for networksearch in network:
    x = networksearch['name']
    if x == networkname:
        networkid = networksearch['id']

# Reading the configuration, removing from the network, adding to the network and configuring the switch per serial number.
for serial in seriallist:
    try:

        # Read Device Information
        RESOURCE = '/networks/' + networkid + '/devices/'+ serial
        call_response = requests.request("GET", base_url + RESOURCE, headers=headers, data={})
        deviceconfig = json.loads(call_response.content)
        print('Read Device Config ' + str(call_response.status_code))
        print('###########')

        # Get all Switch Ports Configuration
        RESOURCE = '/devices/'+ serial + '/switchPorts/'
        call_response = requests.request("GET", base_url + RESOURCE, headers=headers, data={})
        port = json.loads(call_response.content)
        print('Read all Port Config ' + str(call_response.status_code))
        print('###########')


        # Remove Deice from Network
        RESOURCE = '/networks/' + networkid + '/devices/'+ serial + '/remove'
        call_response = requests.request("POST", base_url + RESOURCE, headers=headers, data={})
        print('Remove Device from Network ' + str(call_response.status_code))
        print('###########')

        # Claim Device to the Network
        payload = "{\r\n  \"serials\": [\r\n    \""+ serial + "\"\r\n\r\n  ]\r\n}"
        RESOURCE = '/networks/' + networkid + '/devices/' + '/claim'
        call_response = requests.request("POST", base_url + RESOURCE, headers=headers, data=payload)
        print('Claim Device to the Network ' + str(call_response.status_code))
        print('###########')


        # Write Device Information
        payload = json.dumps(cleanNullTerms(deviceconfig))
        RESOURCE = '/networks/' + networkid + '/devices/'+ serial
        call_response = requests.request("PUT", base_url + RESOURCE, headers=headers, data=payload)
        print('Write Configuration to Device ' + str(call_response.status_code))
        print('###########')


        # Write Switch Port Configuration
        for portid in port:
            payload = json.dumps(cleanNullTerms(portid))
            RESOURCE = '/devices/'+ serial + '/switchPorts/' + str(portid['number'])
            call_response = requests.request("PUT", base_url + RESOURCE, headers=headers, data=payload)
            print('Write Config Port by Port ' + str(portid['number'])  + ' '+ str(call_response.status_code))
            print('###########')

    except:
        print('Error with Serial ' + serial)
        continue
