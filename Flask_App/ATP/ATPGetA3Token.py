import requests
import Logging



def A3token():

    url="https://idmsservice.corp.apple.com/auth/apptoapp/token/generate"
    headers = {'content-type': 'application/json'}

    payload = """{
        "appId": "170622",
        "appPassword": "w87hig8s5iqhyag9",
        "context": "ATP",
        "contextVersion": "1",
        "otherApp": "150088"
        }"""
    Logging.ATPLogger(url,"REQUEST")
    Logging.ATPLogger(headers,"REQUEST")
    Response = requests.request("POST", url, headers=headers, data=payload)
    response = Response.text
    Logging.ATPLogger(response,"RESPONSE")
    A3Token_start = response.find('"token" : "',0)
    A3Token_end = response.find('"',A3Token_start+11)
    ATPToken = response[A3Token_start+11:A3Token_end]
    # Logging.ATPLogger(ATPToken,"RESPONSE")
    return ATPToken

