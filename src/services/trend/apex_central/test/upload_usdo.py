import os
import base64
import jwt
import hashlib
import requests
import time
import json
from api_token import use_url_base, use_application_id, use_api_key
import urllib3
import ipaddress

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
    """From file, read all lines and send a request to Trend Micro Apex Central"""
    filesize = os.path.getsize("ips.txt")
    productAgentAPIPath = '/WebApp/api/SuspiciousObjects/UserDefinedSO/'
    canonicalRequestHeaders = ''
    useQueryString = '' 

    with open("ips.txt") as f:
        if filesize == 0:
            print("The file is empty")
        else:
            for line in f.readlines():
                content = line.strip('\n')
                if len(content) == 40:
                    requestbody = json.dumps( {"param":{"type":"file_sha1","content":content,"notes":"IOC hash added by script","scan_action":"block",}})
                elif ipaddress.ip_address(content):
                    try:
                        requestbody = json.dumps({"param":{"type":"ip","content":content,"notes":"IP address added by script","scan_action":"block",}})
                    except ValueError:
                        print("The value {} does not appear to be an IPv4 or IPv6 address".format(content))

                jwt_token = create_jwt_token(use_application_id, use_api_key, 'PUT',
                                productAgentAPIPath + useQueryString,
                                canonicalRequestHeaders, requestbody, iat=time.time())

                headers = {'Authorization': 'Bearer ' + jwt_token, 'Content-Type': "application/json"}

                r = requests.put(use_url_base + productAgentAPIPath + useQueryString, headers=headers, data=requestbody, verify=False) 
                if r.status_code == 200:
                    print("'{}' added".format(content))
                else:
                    print("There was a problem uploading the content {}, please check the format and try again".format(content))
                
#            print(json.dumps(r.json(), indent=4))

upload_list()