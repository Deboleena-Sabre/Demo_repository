import requests
import Logging


def GetTravelerProfileDetails(ATPToken,BadgeNumber):

    url="https://appletravel.apple.com/api/v1/services/user/profile?"
    headers = {'content-type': 'application/json','X-Apple-Client-App-ID':'170622','X-Apple-Transaction-Id':'1af7eaf9-00f6-47a9-ac55-2995ffbf8bfc','X-Apple-Sender-Id':'gTAD','X-Apple-IDMS-A3-Token':str(ATPToken)}

    payload = """{
    "badgeNumber": """+str(BadgeNumber)+""",
    "gTADEprUserId": "2222-57HG"
    }"""
    
    response = requests.request("POST", url, headers=headers, data=payload)
    Logging.ATPLogger(url,"REQUEST")
    Logging.ATPLogger(headers,"REQUEST")
    Logging.ATPLogger(payload,"REQUEST")
    # print(response.text)
    Response = response.text
    Logging.ATPLogger(Response,"RESPONSE")
    FirstName_start = Response.find('"firstName":"',0)
    # print(FirstName_start)
    FirstName_end = Response.find('"',FirstName_start+13)
    # print(FirstName_end)
    FirstName = Response[FirstName_start+13:FirstName_end]
    LastName_start = Response.find('"lastName":"',0)
    LastName_end =  Response.find('"',LastName_start+12)
    LastName = Response[LastName_start+12:LastName_end]
    # print(FirstName+LastName)
    return FirstName,LastName