# from queue import Queue
# from asyncio.windows_events import NULL
import Logging
import SessionCreate
import SendSabreCommand
import SWSGetReservation


g_pnrHold = ''

#FINISH PROCESS
def finish_process(log_status):
    Logging.logger(log_status)
    print(log_status)

def check_queue():
    pass


QueueNo = "395"
Pcc = "vk87"

BinaryToken = SessionCreate.createSession()
log_status = ("Processing Work Queue")
Logging.logger(log_status)
HostCommand = "qc/"+Pcc+QueueNo
Res = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
Response_start= Res.find("QUEUE "+QueueNo+"  HAS       ")  + 18
# Response_start=Response_start + 18
Response_end = Response_start + 4
Queuecount= Res[Response_start:Response_end]
Queuecount = Queuecount.strip()
print(Queuecount)
if Queuecount == '0':
    log_status ="END OF PROCESS FOR QUEUE-"+QueueNo
    finish_process(log_status)
else:
    log_status="Accessing Queue for Next PNR"
    Logging.logger(log_status)
    HostCommand = "q/"+Pcc+QueueNo
    QueueResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
    Queue_resStart = QueueResponse.find("<Response>") + 10
    # Queue_resStart = Queue_resStart + 10
    Queue_resEnd = QueueResponse.find("</Response>")
    QueueResult = QueueResponse[Queue_resStart:Queue_resEnd]
    Emptycheck = QueueResult.find("QUEUE SELECTED WAS EMPTY")
    if Emptycheck != -1:
        log_status ="QUEUE SELECTED WAS EMPTY"
        finish_process(log_status)
    else:
        Logging.logger(QueueResult)
        print(QueueResult)        
        #Recieved from field
        HostCommand = "*P6"
        RecievedResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        Recieved_resStart = RecievedResponse.find("<Response>") + 10
        Recieved_resEnd = RecievedResponse.find("</Response>")
        RecievedResult = RecievedResponse[Recieved_resStart:Recieved_resEnd]
        str_len = len(RecievedResult)-2
        copy_len = str_len - 6
        HostPNR = RecievedResult[copy_len:str_len]
        Logging.logger('PNR retrieved from Queue -'+HostPNR)
        print("PNR retrieved from Queue -"+HostPNR)
        
        #SWSGetreservationRQ

        Logging.logger("Parsing PNR Data via SWS")
        print("Parsing PNR Data via SWS")
        GetReservation_Response = SWSGetReservation.GetReservationAPI(BinaryToken)
        SWSPNR_start = GetReservation_Response.find("RecordLocator>") + 14
        SWSRecievedPNR = GetReservation_Response[SWSPNR_start:SWSPNR_start+6]
        if SWSRecievedPNR == '':
            lcl_not_processed = 'Y'
            check_queue()
        else:    
            Logging.logger('PNR being processed from SWS -'+ SWSRecievedPNR)
            print("PNR being processed from SWS -"+ SWSRecievedPNR)
            if (SWSRecievedPNR != HostPNR or SWSRecievedPNR == g_pnrHold):
                if (SWSRecievedPNR != HostPNR):
                    Logging.logger("PNR retrieved from Queue and SWS PNR are different")     
                    print("PNR retrieved from Queue and SWS PNR are different")
                    Logging.logger("QueuePNR - "+ HostPNR +" , "  "SWSPNR - " + SWSRecievedPNR)
                    print("QueuePNR - "+ HostPNR +" , "  "SWSPNR - " + SWSRecievedPNR)
                # else:
                #     Logging.logger



