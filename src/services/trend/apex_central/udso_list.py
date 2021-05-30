import base64
import jwt
import hashlib
import requests
import time
import json
import urllib.parse

"""def payload(payload):
    domain_type = print(input("Ingrese dominio: " ))
    content_filter = print(input("Ingrese filtro: "))

    payload = "?type=" + domain_type + "&contentFilter= " + content_filter
    return payload
    
    #useQueryString="?type=Domain&contentFilter=decryptor.top"
    
r = requests.get(use_url_base + productAgentAPIPath + useQueryString, headers=headers, verify=False)
"""


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
	
# Use this region to setup the call info of the Apex Central server (server url, application id, api key)

# server info
def udso_list():
    domain_type = str(input("Ingrese Dominio: "))
    content_filter = str(input("Ingrese Filtro: "))
    use_url_base = 'SERVER_NAME' 
    use_application_id = 'Application_ID'
    use_api_key = 'API_KEY'

    productAgentAPIPath = '/WebApp/api/SuspiciousObjects/UserDefinedSO/'
    canonicalRequestHeaders = ''

    useRequestBody = ''

    useQueryString = str("?type=" + domain_type + "&contentFilter=" + content_filter)
    #useQueryString="?type=Domain&contentFilter=decryptor.top"
    #useQueryString="?type=ip&contentFilter=168.95"
    jwt_token = create_jwt_token(use_application_id, use_api_key, 'GET',
                                productAgentAPIPath + useQueryString,
                                canonicalRequestHeaders, useRequestBody, iat=time.time())

    headers = {'Authorization': 'Bearer ' + jwt_token , 'Content-Type': 'application/json;charset=utf-8'}
    #Choose by call type.Doa
    r = requests.get(use_url_base + productAgentAPIPath + useQueryString, headers=headers, verify=False)

    print(r.status_code)
    print(json.dumps(r.json(), indent=4))

#udso_list()
#domain_type = str(input("Ingrese Dominio: "))
#content_filter = str(input("Ingrese Filtro: "))

#udso_list(domain_type,content_filter)
