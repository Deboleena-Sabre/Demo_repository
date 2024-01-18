import Logging
import SendSabreCommand
import GetRemarkDetailsResponse
import SWSGetReservation
from ATP import ATPGetA3Token,ATPGetTravelerProfileDetails
import mysql.connector
import pandas as pd
import OPA_retrieveResponse
import OPA_ignore


def GetRemarkLineNumber(remarkSearchString,df):
    remarklineNo = ''
    for x in range(len(df)):
        remarkTemp = df.RemarkText[x]
        pos = remarkTemp.find(remarkSearchString)
        if(pos!=-1):
            remarklineNo = x+1
            break

    return remarklineNo


def pnrProcess(Pcc, SWSRecievedPNR, BinaryToken, QueueNo, GetReservation_Response, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn):
    # RecordCounter = ''
    Logging.logger("PROCESSING RECORD # -"+SWSRecievedPNR)
    print("PROCESSING RECORD # -"+SWSRecievedPNR)

    # RecordCounter = RecordCounter + 1

    #Display PNR
    HostCommand = "*"+SWSRecievedPNR
    PNRInfo= SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
    PNRInfo = OPA_retrieveResponse.Response_Block(PNRInfo,10)
    BadgeNumberCheck = PNRInfo.find("S*UD5 ",0)
    if BadgeNumberCheck !=-1:
        Badge_end = PNRInfo.find(" ",BadgeNumberCheck+6)
        BadgeNumber = PNRInfo[BadgeNumberCheck+6:Badge_end]
        print("BadgeNumber = " + BadgeNumber)
        ATPToken = ATPGetA3Token.A3token()
        FirstName,LastName = ATPGetTravelerProfileDetails.GetTravelerProfileDetails(ATPToken,BadgeNumber)
        if FirstName != '' and LastName != '':
            SabreCommand = "5 ATP found for "+FirstName + " " + LastName 
            CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
            # print("5 ATP found for "+FirstName + " " + LastName)
            Logging.logger("ATP found for "+FirstName + " " + LastName)
        else:
            SabreCommand = "5 ATP not found"  
            CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
            # print("5 ATP not found")
            Logging.logger("ATP not found")

        

    # Logging.logger(PNRInfo)
    PNRInfo_present = PNRInfo.find("SIGN IN")
    if PNRInfo_present !=-1:
        Logging.logger("APPLICATION IS NOT SIGNED IN - APPROVALROBOT PROCESSING HALTED")
        print("APPLICATION IS NOT SIGNED IN - APPROVALROBOT PROCESSING HALTED")
        notsignIn_flag = '1'
        # ApprovalStatus, secondAttemptFlag, finish_flag, signIn_flag
        return '', '' , '' , notsignIn_flag

    PNRInfo_Start = PNRInfo.find("1.")
    ReceivedRecord =PNRInfo[PNRInfo_Start:PNRInfo_Start+2]
    if ReceivedRecord == '':
        Logging.logger("UNABLE TO RETRIEVE RECORD FOR LOCATOR #"+SWSRecievedPNR)
        print("UNABLE TO RETRIEVE RECORD FOR LOCATOR #"+SWSRecievedPNR)
        lcl_not_processed = 'Y'

        # ignore(QueueNo, BinaryToken, g_pnrHold, tryAgainFlag)
        finish_flag = OPA_ignore.ignore(Pcc, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
        return '', tryAgainFlag, finish_flag, notsignIn_flag

    else:

        # # Database connection
        # mydb = mysql.connector.connect(
        # host="17.129.253.37",
        # user="parameswaran",
        # password="Sundaramoorthyd8de",
        # database="dev"
        # )

        # print(mydb)
        db_conn.commit()
        mycursor = db_conn.cursor()
        query = "SELECT unibox_approval_status,PNR_BCN FROM fmdbopalist_copy where PNR_BCN= "+"'" + SWSRecievedPNR +"'"
        mycursor.execute(query)
        Logging.logger("Current Query :" + query)
        print("Current Query :" + query)
        myresult = mycursor.fetchall()

        OPAStatusDetails = pd.DataFrame(myresult)
        OPAStatusDetails.columns = ['UniboxApprovalStatus', 'PNR_BCN']

        Logging.logger("Current Data Fetched : " + str(myresult))
        print("Current Data Fetched : " + str(myresult))

        RowCount = len(OPAStatusDetails)
        # RowCount = 1
        if RowCount >=1:
            # ApprovalStatus="Denied"
            ApprovalStatus = OPAStatusDetails['UniboxApprovalStatus'].iloc[0]
            if ((ApprovalStatus == '') or (ApprovalStatus=='Pending')):
                Logging.logger("OPA status found as Blank/Pending")
                print("OPA status found as Blank/Pending")
                Logging.logger("OPA Status blank/Pending ignoring PNR - "+ SWSRecievedPNR)
                print("OPA Status blank/Pending ignoring PNR - "+ SWSRecievedPNR)
                Logging.logger("Ignoring the PNR - I")
                print("Ignoring the PNR - I")
                finish_flag = OPA_ignore.ignore(Pcc, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)

                return ApprovalStatus, tryAgainFlag, finish_flag, notsignIn_flag

            else:
                RemarkDetailsDF = GetRemarkDetailsResponse.createRemarkDataFrame(GetReservation_Response)
                if ApprovalStatus=='Denied':
                    Logging.logger("OPA status found as Denied")
                    print("OPA status found as Denied")
                    SearchString = 'OPA APPROVAL '
                    RemarkLineNumber = GetRemarkLineNumber(SearchString,RemarkDetailsDF)
                    # Logging.logger(str(RemarkLineNumber))
                    if RemarkLineNumber != '':
                        Logging.logger("Deleting existing remarks")
                        print("Deleting existing remarks")
                        SabreCommand = "5"+str(RemarkLineNumber)+"\u0080" #unicode for CHANGE key
                        CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                    Logging.logger('Adding Denied K¥ remarks')
                    print("Adding Denied K¥ remarks")
                    SabreCommand = "5K\u0081OPA APPROVAL DENIED"  #unicode for CROSS OF LORRAIN key
                    CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                    # Logging.logger(CommandResponse)
                    Logging.logger('Adding Denied 5H remarks')
                    print("Adding Denied 5H remarks")
                    SabreCommand = "5H-APPROB IDENTIFIED OPA DENIED BY AN APPROVER"
                    CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                    CommandResponse = OPA_retrieveResponse.Response_Block(CommandResponse,10)
                    # Logging.logger(CommandResponse)

                elif ApprovalStatus == 'Approved':
                    Logging.logger('OPA status found as Approved')
                    print("OPA status found as Approved")
                    SearchString = 'S*UD56 '
                    RemarkLineNumber = GetRemarkLineNumber(SearchString,RemarkDetailsDF)
                    if RemarkLineNumber != '':
                        Logging.logger("Deleting existing remarks")
                        print("Deleting existing remarks")
                        SabreCommand = "5"+str(RemarkLineNumber)+"\u0080" #unicode for CHANGE key
                        Logging.logger(SabreCommand)
                        CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                        Logging.logger(CommandResponse)                            
                        print(CommandResponse)
                        Logging.logger("Parsing PNR Data for fresh update")
                        print("Parsing PNR Data for fresh update")
                        GetReservation_Res = SWSGetReservation.GetReservationAPI(BinaryToken)
                        Logging.logger(GetReservation_Res)                            
                        print(GetReservation_Res)

                    
                    SearchString = "OPA APPROVAL "
                    RemarkLineNumber = GetRemarkLineNumber(SearchString,RemarkDetailsDF)
                    print(RemarkLineNumber)
                    Logging.logger(str(RemarkLineNumber))
                    if RemarkLineNumber != '':
                        Logging.logger("Deleting existing remarks")
                        print("Deleting existing remarks")
                        SabreCommand = "5"+str(RemarkLineNumber)+"\u0080" #unicode for CHANGE key
                        CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                        Logging.logger(CommandResponse)

                    Logging.logger('Adding Approved K¥ remarks')
                    print('Adding Approved K¥ remarks')
                    SabreCommand = "5K\u0081OPA APPROVAL APPROVED" #unicode for CROSS OF LORRAIN key
                    CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                    Logging.logger('Adding Approved 5H remarks')
                    print('Adding Approved 5H remarks')
                    SabreCommand = "5H-APPROB IDENTIFIED OPA FULLY APPROVED"
                    CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)
                    Logging.logger('Adding Approved S*UD56 remarks')
                    print('Adding Approved S*UD56 remarks')
                    SabreCommand = "5.S*UD56 APPROVED"
                    CommandResponse = SendSabreCommand.SendSabreAPI(BinaryToken,SabreCommand)


        secondAttemptFlag = ''
        Logging.logger("Saving Remarks in the PNR")
        print("Saving Remarks in the PNR")
        Recieved_From = "6TEST"      #used 6TEST for testing...->should be 6OPAROBOT
        SendSabreCommand.SendSabreAPI(BinaryToken,Recieved_From)
        Logging.logger(Recieved_From)
        print(Recieved_From)

        return ApprovalStatus, secondAttemptFlag, finish_flag, notsignIn_flag