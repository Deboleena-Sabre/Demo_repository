import requests
import Logging
import SessionCreate

def SendSabreAPI(BinaryToken,HostCommand):

    url="https://webservices.platform.sabre.com/websvc"

    headers = {'content-type': 'text/xml'}


    payload = """<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://schemas.xmlsoap.org/ws/2002/12/secext" xmlns:mes="http://www.ebxml.org/namespaces/messageHeader" xmlns:ns="http://webservices.sabre.com/sabreXML/2003/07">
    <soapenv:Header>
        <sec:Security>
            <sec:BinarySecurityToken>"""+BinaryToken+"""</sec:BinarySecurityToken>
        </sec:Security>
        <mes:MessageHeader mes:id="?" mes:version="?">
            <mes:From>
                <mes:PartyId type="urn:x12.org:IO5:01">Turbo</mes:PartyId>
            </mes:From>
            <mes:To>
                <mes:PartyId  type="urn:x12.org:IO5:01">webservices.sabre.com</mes:PartyId>
            </mes:To>
            <mes:CPAId>57HG</mes:CPAId>
            <mes:ConversationId>2021-02-04-11184</mes:ConversationId>
            <mes:Service mes:type="sabreXML">Session</mes:Service>
            <mes:Action>SabreCommandLLSRQ</mes:Action>
            <mes:MessageData>
                <mes:MessageId>mid:1000</mes:MessageId>
                <mes:Timestamp>2022-12-04T18:27:23Z</mes:Timestamp>
                <mes:TimeToLive>2022-12-04T18:57:23Z</mes:TimeToLive>
            </mes:MessageData>
        </mes:MessageHeader>
    </soapenv:Header>
    <soapenv:Body>
        <ns:SabreCommandLLSRQ >
            <ns:Request Output="SCREEN" MDRSubset="?" CDATA="false">
                <ns:HostCommand>"""+ HostCommand +"""</ns:HostCommand>
            </ns:Request>
        </ns:SabreCommandLLSRQ>
    </soapenv:Body>
    </soapenv:Envelope>""" 
    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    Res = response.text
    TokenCheck = Res.find("Invalid or Expired binary security token")
    if TokenCheck != -1:
        # print("TokenCheck :"+ str(TokenCheck))
        # print("Invalid or Expired binary security token")
        BinaryToken = SessionCreate.createSession()
        # print("New Binary Token" + BinaryToken)
        Res = SendSabreAPI(BinaryToken,HostCommand)
    Logging.OPASWSLogger(payload, "REQUEST")
    # Res = response.text
    Logging.OPASWSLogger(Res, "RESPONSE")
    return Res

    



