import Logging
import SendSabreCommand

import OPA_checkQueue
import OPA_retrieveResponse



def resend(Pcc, BinaryToken, ticketingLimitFixAttemptFlag, secondAttemptFlag, ApprovalStatus, QueueNo, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, db_conn):
    HostCommand ="ER"
    Logging.logger(HostCommand)
    print(HostCommand)
    End_Retreive = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
    End_Retreive = OPA_retrieveResponse.Response_Block(End_Retreive,10)
    Logging.logger(End_Retreive)
    print(End_Retreive)

    #*** Fix for Ticketing Limit Issue. ***
    TimeLimit = End_Retreive.find("TICKET/TIMELIMIT MUST PRECEDE TRAVEL DATE")
    if TimeLimit != -1:
        if ticketingLimitFixAttemptFlag == '':
            Logging.logger("Replacing TAW line with Current Date...")
            print("Replacing TAW line with Current Date...")
            HostCommand = "7TAW/OPA"
            Response = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
            Response = OPA_retrieveResponse.Response_Block(Response,10)
            Logging.logger(Response)
            ticketingLimitFixAttemptFlag = "Y"
            if secondAttemptFlag == '':
                secondAttemptFlag = "Y"
                ###GOTO RESEND
    ticketingLimitFixAttemptFlag = ''
    # er_end_record_check(ticketingLimitFixAttemptFlag)
    if ticketingLimitFixAttemptFlag == "Y":
        if secondAttemptFlag == '':
            secondAttemptFlag = "Y"
            ###GOTO RESEND
        
    if ApprovalStatus == "Approved":
        HostCommand = "QP/" + Pcc +"116/11"
        Logging.logger(HostCommand)
        print(HostCommand)
        Response = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        Response = OPA_retrieveResponse.Response_Block(Response,10)
        # QueueResult, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken
        finish_flag = OPA_checkQueue.check_queue(Pcc, Response, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
    elif  ApprovalStatus == "Denied":
        HostCommand = "QP/" + Pcc +"116/11"
        Logging.logger(HostCommand)
        print(HostCommand)
        Response = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        Response = OPA_retrieveResponse.Response_Block(Response,10)
        finish_flag = OPA_checkQueue.check_queue(Pcc, Response, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
        # print(Response)

    return finish_flag