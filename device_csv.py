import csv 
import requests
import yaml

try:
    with open('kentik.yaml', 'r') as file:
        yamlcfg = yaml.safe_load(file)
except Exception as e:
    print(e)

site = yamlcfg['kentik_auth']['api_url']
device_url = site + '/api/v5/device/'
plan_id = yamlcfg['kentik_auth']['planid']
kentik_email = yamlcfg['kentik_auth']['X-CH-Auth-Email']
kentik_api_token = yamlcfg['kentik_auth']['X-CH-Auth-API-Token']



headers = {
    'X-CH-Auth-Email': kentik_email,
    'X-CH-Auth-API-Token': kentik_api_token,
    'Content-Type' : yamlcfg['kentik_auth']['Content-Type'],
}


with open('devices.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        json_object = {
            "device": { 
                "device_name": row['device_name'],
                "device_type": 'router',
                "device_description": row['device_name'],
                "plan_id": plan_id,
                "device_sample_rate":1,
                "sending_ips":[row['flow_ip']],
                "device_snmp_ip":row['snmp_ip'],
                "device_snmp_community":row['snmp_community'],
                 "device_bgp_type": "none",
                 "minimize_snmp": False
            }
        }
        response = requests.post(device_url, headers=headers,  json=json_object)

        if "error" in response.json():
            print(row['device_name'])
            print(response.text)
        else:
            print("success!: " + row['device_name'])
            #print(response.text) 
        
        