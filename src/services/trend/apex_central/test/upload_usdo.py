import os
import base64
import jwt
import hashlib
import requests
import time
import json
from api_token import use_url_base, use_application_id, use_api_key
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_checksum(http_method, raw_url, headers, request_body):
    string_to_hash = http_method.upper() + '|' + raw_url.lower() + '|' + headers + '|' + request_body
    base64_string = base64.b64encode(hashlib.sha256(str.encode(string_to_hash)).digest()).decode('utf-8')
    return base64_string

def create_jwt_token(appication_id, api_key, http_method, raw_url, headers, request_body,
                     iat=time.time(), algorithm='HS256', version='V1'):
    payload = {'appid': appication_id,
               'iat': iat,
               'version': version,
               'checksum': create_checksum(http_method, raw_url, headers, request_body)}
    token = jwt.encode(payload, api_key, algorithm=algorithm)
    return token 

def upload_list():
    """Recorre archivo y envia los request"""
    filesize = os.path.getsize("ips.txt")
    productAgentAPIPath = '/WebApp/api/SuspiciousObjects/UserDefinedSO/'
    canonicalRequestHeaders = ''
    useQueryString = '' 

    with open("ips.txt") as f:
        if filesize == 0:
            print("The file is empty")
        else:
            for line in f.readlines():
                ip = line.strip('\n')
                ip_list = {
                "param":{
                    "type":"ip",
                    "content":ip,
                    "notes":"Suspicious IP address added by script",
                    "scan_action":"block",
                    }
                }
                useRequestBody = json.dumps(ip_list)
                
                jwt_token = create_jwt_token(use_application_id, use_api_key, 'PUT',
                                productAgentAPIPath + useQueryString,
                                canonicalRequestHeaders, useRequestBody, iat=time.time())

                headers = {'Authorization': 'Bearer ' + jwt_token, 'Content-Type': "application/json"}

                r = requests.put(use_url_base + productAgentAPIPath + useQueryString, headers=headers, data=useRequestBody, verify=False) 
                if r.status_code == 200:
                    print("The IP {} has been added".format(ip))
                else:
                    print("There was a problem uploading the IP {}, please check the format (ie: 192.168.1.1)".format(ip))
                
#            print(json.dumps(r.json(), indent=4))

upload_list()