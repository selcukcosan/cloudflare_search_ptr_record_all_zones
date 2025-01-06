import json
import requests
import pprint
from datetime import datetime

cloudflare_api = "https://api.cloudflare.com/client/v4/"

api_token = "Bearer XXXXXXXXXXXXXXXXXXXXXXXXXX"
headers = {'Authorization': api_token, 'Content-Type':'application/json'}

ptr_id = "192.0.2.1"
result= ""
cloudflare_dns = cloudflare_api + "zones?page=1&per_page=500"
cloudflare_dns_response = requests.get(cloudflare_dns, headers=headers)

if cloudflare_dns_response.status_code == 200:
    all_zones_data = json.loads(cloudflare_dns_response.text)
    line_count = 0
    for zones in all_zones_data["result"]:
        line_count += 1
        zone_name = zones["name"]
        zone_id = zones["id"]
        cloudflare_dns = cloudflare_api + "zones/" + zone_id + "/dns_records"
        cloudflare_dns_response = requests.get(cloudflare_dns, headers=headers)
        print(ptr_id+" searching for "+str(line_count)+" "+zone_name)

        if cloudflare_dns_response.status_code == 200:
            dns_data = json.loads(cloudflare_dns_response.text)

            for names in dns_data["result"]:
                content = names["content"]
                if content == ptr_id:
                    result += names["name"]+" "
                    #print(ptr_id+" PTR Record has been found in "+line_count+" "+zone_name)
            #if result == "":
                #print(ptr_id+" PTR Record has not been found in "+line_count+" "+zone_name)
        else:
            print(cloudflare_dns_response.status_code)
else:
    print(cloudflare_dns_response.status_code)

print(ptr_id+" results "+result)
