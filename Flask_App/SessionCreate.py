import requests
import Logging
import getSignInDetails


def createSession():
    credDict = getSignInDetails.SignInDetails()
    url="https://webservices.platform.sabre.com/websvc"

    headers = {'content-type': 'text/xml'}


    payload = """<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope
        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:eb="http://www.ebxml.org/namespaces/messageHeader"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        xmlns:xsd="http://www.w3.org/1999/XMLSchema">
        <SOAP-ENV:Header>
            <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="2.0">
                <eb:ConversationId>2021-02-04-11184</eb:ConversationId>
                <eb:From>
                    <eb:PartyId type="urn:x12.org:IO5:01">Turbo</eb:PartyId>
                </eb:From>
                <eb:To>
                    <eb:PartyId type="urn:x12.org:IO5:01">webservices.sabre.com</eb:PartyId>
                </eb:To>
                <eb:CPAId>57HG</eb:CPAId>
                <eb:Service eb:type="sabreXML">Session</eb:Service>
                <eb:Action>SessionCreateRQ</eb:Action>
                <eb:MessageData>
                    <eb:MessageId>mid:1000</eb:MessageId>
                    <eb:Timestamp>2022-12-04T18:27:23Z</eb:Timestamp>
                    <eb:TimeToLive>2022-12-04T18:57:23Z</eb:TimeToLive>
                </eb:MessageData>
            </eb:MessageHeader>
            <wsse:Security
                xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext"
                xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility">
                <wsse:UsernameToken>
                    <wsse:Username>"""+credDict['Username']+"""</wsse:Username>
                    <wsse:Password>"""+credDict['Password']+"""</wsse:Password>
                    <Organization>57HG</Organization>
                    <Domain>AA</Domain>
                </wsse:UsernameToken>
            </wsse:Security>
        </SOAP-ENV:Header>
        <SOAP-ENV:Body>
            <SessionCreateRQ returnContextID="true">
                <POS>
                    <Source PseudoCityCode="57HG"/>
                </POS>
            </SessionCreateRQ>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>""" 
    response = requests.request("POST", url, headers=headers, data=payload)

    Logging.OPASWSLogger(payload, "REQUEST")
    Response=response.text
    
    Logging.OPASWSLogger(Response, "RESPONSE")
    # print(Response)
    Token_start = Response.find('Shared',0)
    Token_end = Response.find('</wsse:BinarySecurityToken>',Token_start)
    BinaryToken = Response[Token_start:Token_end] 
    # print(BinaryToken)
    return BinaryToken 
