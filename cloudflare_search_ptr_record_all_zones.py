import json
import requests
import pprint
from datetime import datetime

cloudflare_api = "https://api.cloudflare.com/client/v4/"

api_token = "Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
headers = {'Authorization': api_token, 'Content-Type':'application/json'}

ptr_id = "192.168.1.1"
per_page = 500
result= ""
print("Loading Zones")
cloudflare_dns = cloudflare_api + "zones?page=1&per_page=" + str(per_page)
cloudflare_dns_response = requests.get(cloudflare_dns, headers=headers)

if cloudflare_dns_response.status_code == 200:
    all_zones_data = json.loads(cloudflare_dns_response.text)
    #pprint.pprint(all_zones_data["result_info"])
    total_pages = all_zones_data["result_info"]["total_pages"] 
    number_of_zones =  all_zones_data["result_info"]["total_count"]
    print("Number of Zones: "+ str(number_of_zones) + " Per Page: "+str(per_page)+" Number of Pages: " + str(total_pages))

    line_count = 0
    for page_number in range(total_pages):
        page_number += 1
        print("Getting Page: "+ str(page_number))
        
        cloudflare_dns = cloudflare_api + "zones?page="+ str(page_number) +"&per_page=" + str(per_page)
        cloudflare_dns_response = requests.get(cloudflare_dns, headers=headers)

        if cloudflare_dns_response.status_code == 200:

            all_zones_data = json.loads(cloudflare_dns_response.text)
            pprint.pprint(all_zones_data["result_info"])
            

            for zones in all_zones_data["result"]:
                line_count += 1
                zone_name = zones["name"]
                zone_id = zones["id"]
                cloudflare_dns = cloudflare_api + "zones/" + zone_id + "/dns_records?page=1&per_page=5000&content="+ptr_id
                #pint(cloudflare_dns)
                cloudflare_dns_response = requests.get(cloudflare_dns, headers=headers)       
                print("Searching Zone: "+str(line_count)+" "+zone_name + " for "+ptr_id)
                iffound = False
                if cloudflare_dns_response.status_code == 200:
                    dns_data = json.loads(cloudflare_dns_response.text)
                    for names in dns_data["result"]:
                        content = names["content"]
                        if content == ptr_id:
                            result += names["name"]+" "
                            iffound = True
                            #print(ptr_id+" PTR Record has been found in "+str(line_count)+" "+zone_name)
                    if iffound:
                        pprint.pprint(dns_data)
                else:
                    print(cloudflare_dns_response.status_code)                  
        else:
            print(cloudflare_dns_response.status_code)    


    else:
        print(cloudflare_dns_response.status_code)     


print(ptr_id+" results "+result)
