# from queue import Queue
# from asyncio.windows_events import NULL
import Logging
import SessionCreate
import SendSabreCommand
import SWSGetReservation
import CheckEmptyQueue
import mysql.connector
import pandas as pd
import GetRemarkDetailsResponse


import enterQueue
import OPA_nextPnr
import OPA_PnrProcessing
import OPA_resend
import OPA_checkQueue
import OPA_finishProcess
import time


def OPARobotProcessing(Pcc, db_conn):
    ticketingLimitFixAttemptFlag = ''
    g_pnrHold = ''
    tryAgainFlag = ''
    RecordCounter = ''
    finish_flag = '0'
    notsignIn_flag = '0'

    print("Initiating OPA process")
    Logging.logger("Initiating OPA process")

    QueueNo = "117"
    # Pcc = "VK87"

    BinaryToken = SessionCreate.createSession()
    Logging.logger(BinaryToken)
    Logging.logger("Processing Work Queue")
    print("Processing Work Queue")
    print("COUNTING RECORDS IN WORK QUEUE "+ Pcc +" "+QueueNo)
    Logging.logger("COUNTING RECORDS IN WORK QUEUE "+ Pcc +" "+QueueNo)
    HostCommand = "qc/"+Pcc+QueueNo
    Res = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
    Response_start= Res.find("QUEUE "+QueueNo+"  HAS       ")  + 18
    # Response_start=Response_start + 18
    Response_end = Response_start + 4
    Queuecount= Res[Response_start:Response_end]
    Queuecount = Queuecount.strip()
    Queuecount_status = ("QUEUE "+QueueNo+" HAS " + Queuecount + " PNR")
    print(Queuecount_status)
    Logging.logger(Queuecount_status)
    if Queuecount == '0':
        finish_flag = OPA_finishProcess.finish_process(QueueNo, finish_flag)
    else:

        # calling enterQueue
        QueueResult = enterQueue.EnterQueue(Pcc, QueueNo, BinaryToken)
        

        # calling nextPNR
        SWSRecievedPNR, GetReservation_Response, g_pnrHold, tryAgainFlag, finish_flag  = OPA_nextPnr.nextPnr(Pcc, QueueResult, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)


        # calling process
        if finish_flag=='0':
            ApprovalStatus, secondAttemptFlag, finish_flag, notsignIn_flag = OPA_PnrProcessing.pnrProcess(Pcc, SWSRecievedPNR, BinaryToken, QueueNo, GetReservation_Response, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)


        # calling resend
        if notsignIn_flag == '0' and finish_flag=='0':
            finish_flag = OPA_resend.resend(Pcc, BinaryToken, ticketingLimitFixAttemptFlag, secondAttemptFlag, ApprovalStatus, QueueNo, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, db_conn)


    time.sleep(60)