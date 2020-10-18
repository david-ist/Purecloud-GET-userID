import base64, requests, sys
import pprint

# Request oauth token  referene: https://developer.inindca.com/api/tutorials/oauth-client-credentials/?language=python&step=1
client_id = "XXXXXXXXXXX"  
client_secret = "XXXXXXXXXXXXXXXXX"  

authorization = base64.b64encode(bytes(client_id + ":" + client_secret, "ISO-8859-1")).decode("ascii")

request_headers = {
    "Authorization": f"Basic {authorization}",
    "Content-Type": "application/x-www-form-urlencoded"
}
request_body = {
    "grant_type": "client_credentials"
}

response = requests.post("https://login.mypurecloud.com/oauth/token", data=request_body, headers=request_headers)

if response.status_code == 200:
    print("Token generated")
else:
    print(f"Failure: { str(response.status_code) } - { response.reason }")
    sys.exit(response.status_code)

response_json = response.json()

# Header
requestHeaders = {
    "Authorization": f"{ response_json['token_type'] } { response_json['access_token']}"
}

# query for username

query = {
  "pageSize": 25,
  "pageNumber": 1,
  "types": [
    "users"
  ],
  "sortOrder": "SCORE",
  "query": [
    {
      "type": "TERM",
      "fields": [
        "name",
        "id"
      ],
      "operator": "AND",
      "value": "USERNAME"
    }
    ]
    }

# POST user search
response = requests.post("https://api.mypurecloud.com/api/v2/users/search", json = query, headers=requestHeaders)

# get the ID value from the response JSON
if response.status_code >= 200 and  response.status_code <= 299:
    jsonresult=response.json()
    result = jsonresult['results']
    r2 = result[0]
    userid = list(r2.values())[0]
else:
    print(response.status_code)

#Get user routing skills

r = requests.get(F"https://api.mypurecloud.com/api/v2/users/{userid}/routingskills", headers=requestHeaders)

if r.status_code == 200:
    jsonresult=r.json()
    pprint.pprint(jsonresult)
else:
    print(f"Failure: { str(r.status_code) } - { r.reason }")
    sys.exit(r.status_code)


# delete our oauth token
r = requests.delete("https://api.mypurecloud.com/api/v2/tokens/me", headers=requestHeaders)
if r.status_code >= 200 and  r.status_code <= 299:
    print("Token Destroyed")
else:
    print(r.text)
    exit()
