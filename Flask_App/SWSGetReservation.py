import requests
import Logging
import SessionCreate

def GetReservationAPI(BinaryToken):
    url="https://webservices.platform.sabre.com/websvc"

    headers = {'content-type': 'text/xml'}

    payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://schemas.xmlsoap.org/ws/2002/12/secext" xmlns:mes="http://www.ebxml.org/namespaces/messageHeader" xmlns:v1="http://webservices.sabre.com/pnrbuilder/v1_19" xmlns:v11="http://services.sabre.com/res/or/v1_14">
    <soapenv:Header>
        <sec:Security>
            <sec:BinarySecurityToken>"""+BinaryToken+"""</sec:BinarySecurityToken>
        </sec:Security>
        <mes:MessageHeader>
            <mes:From>
                <mes:PartyId mes:type="urn:x12.org:IO5:01">SWS</mes:PartyId>
            </mes:From>
            <mes:To>
                <mes:PartyId mes:type="urn:x12.org:IO5:01">SWS</mes:PartyId>
            </mes:To>
            <mes:CPAId>2B67</mes:CPAId>
            <mes:ConversationId>02da9322-8f6d-415b-a40f-46f8ed0419n6</mes:ConversationId>
            <mes:Service>GetReservationRQ</mes:Service>
            <mes:Action>GetReservationRQ</mes:Action>
            <mes:MessageData>
                <mes:MessageId>d9424771-cfc8-4258-a666-c9f516eb48e8</mes:MessageId>
                <mes:Timestamp>2018-05-01T23:25:48</mes:Timestamp>
            </mes:MessageData>
        </mes:MessageHeader>
    </soapenv:Header>
    <soapenv:Body>
        <v1:GetReservationRQ Version="1.19.0" >
            <v1:RequestType>Stateful</v1:RequestType>
            <v1:ReturnOptions UnmaskCreditCard="false" ShowTicketStatus="false" IncludePaymentCardToken="false">
                <v1:ResponseFormat>STL</v1:ResponseFormat>
            </v1:ReturnOptions>
        </v1:GetReservationRQ>
    </soapenv:Body>
    </soapenv:Envelope>"""
    response = requests.request("POST", url, headers=headers, data=payload)
    Res = response.text
    TokenCheck = Res.find("Invalid or Expired binary security token")
    if TokenCheck != -1:
        # print("TokenCheck :"+ str(TokenCheck))
        # print("Invalid or Expired binary security token")
        BinaryToken = SessionCreate.createSession()
        # print("New Binary Token" + BinaryToken)
        Res = GetReservationAPI(BinaryToken)

    Logging.OPASWSLogger(payload, "REQUEST")
    Logging.OPASWSLogger(Res, "RESPONSE")

    return response.text