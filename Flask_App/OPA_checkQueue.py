import Logging
import CheckEmptyQueue
import OPA_finishProcess
import OPA_nextPnr

import OPA_PnrProcessing
import OPA_resend

def check_queue(Pcc, QueueResult, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn):
    Empty_Queue = CheckEmptyQueue.checkQueue(QueueResult, QueueNo, BinaryToken)

    # Logging.logger(QueueResult)
    # print(QueueResult)
    
    
    if Empty_Queue != "Y":
        # QueueResult, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag
        SWSRecievedPNR, GetReservation_Response, g_pnrHold, tryAgainFlag, finish_flag = OPA_nextPnr.nextPnr(Pcc, QueueResult, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn) 
        if finish_flag=='0':
            ApprovalStatus, secondAttemptFlag, finish_flag, notsignIn_flag = OPA_PnrProcessing.pnrProcess(Pcc, SWSRecievedPNR, BinaryToken, QueueNo, GetReservation_Response, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
        if notsignIn_flag == '0' and finish_flag=='0':
            finish_flag = OPA_resend.resend(Pcc, BinaryToken, ticketingLimitFixAttemptFlag, secondAttemptFlag, ApprovalStatus, QueueNo, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, db_conn)
    else:    
        finish_flag = OPA_finishProcess.finish_process(QueueNo, finish_flag)
        
    return finish_flag