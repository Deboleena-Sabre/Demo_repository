
import Logging
import SendSabreCommand
import OPA_checkQueue

# QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag
def ignore(Pcc, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn):
    HostCommand = "I"
    Logging.logger(HostCommand)
    print(HostCommand)
    Ignore_Response = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
    Ignore_resStart = Ignore_Response.find("<Response>") + 10
    Ignore_resEnd = Ignore_Response.find("</Response>")
    Ignore_Response = Ignore_Response[Ignore_resStart:Ignore_resEnd]
    Logging.logger(Ignore_Response)
    print(Ignore_Response)


    # QueueResult, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken
    finish_flag = OPA_checkQueue.check_queue(Pcc, Ignore_Response,g_pnrHold,tryAgainFlag,QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
    return finish_flag