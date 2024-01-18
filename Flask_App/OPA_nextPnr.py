import Logging
import SendSabreCommand
import SWSGetReservation

import OPA_finishProcess
import OPA_checkQueue

import OPA_retrieveResponse



def nextPnr(Pcc, QueueResult, QueueNo, BinaryToken, g_pnrHold, tryAgainFlag, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn):
    Logging.logger('Processing Next PNR from Queue')
    print('Processing Next PNR from Queue')
    Emptycheck = QueueResult.find("QUEUE SELECTED WAS EMPTY")
    if Emptycheck != -1:
        finish_flag = OPA_finishProcess.finish_process(QueueNo)
        return '', '', g_pnrHold, tryAgainFlag, finish_flag
    else:
        print(QueueResult)        
        Logging.logger(QueueResult)
        #Recieved from field
        HostCommand = "*P6"
        RecievedResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        # Recieved_resStart = RecievedResponse.find("<Response>") + 10
        # Recieved_resEnd = RecievedResponse.find("</Response>")
        # RecievedResult = RecievedResponse[Recieved_resStart:Recieved_resEnd]
        RecievedResult = OPA_retrieveResponse.Response_Block(RecievedResponse,10)
        str_len = len(RecievedResult)-2
        copy_len = str_len - 6
        HostPNR = RecievedResult[copy_len:str_len]
        Logging.logger('PNR retrieved from Queue -'+HostPNR)
        print("PNR retrieved from Queue -"+HostPNR)
        
        #SWSGetreservationRQ
        if HostPNR == '':
            # QueueResult, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken
            finish_flag = OPA_checkQueue.check_queue(Pcc, RecievedResult, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
        else:
            Logging.logger("Parsing PNR Data via SWS")
            print("Parsing PNR Data via SWS")
            GetReservation_Response = SWSGetReservation.GetReservationAPI(BinaryToken)
            SWSPNR_start = GetReservation_Response.find("RecordLocator>") + 14
            SWSRecievedPNR = GetReservation_Response[SWSPNR_start:SWSPNR_start+6]
            
            if SWSRecievedPNR == '':
                lcl_not_processed = 'Y'
                finish_flag = OPA_checkQueue.check_queue(Pcc, RecievedResult, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
            else:
                Logging.logger('PNR being processed from SWS - '+ SWSRecievedPNR)
                print("PNR being processed from SWS - "+ SWSRecievedPNR)
                if (SWSRecievedPNR != HostPNR or SWSRecievedPNR == g_pnrHold):
                    if (SWSRecievedPNR != HostPNR):
                        Logging.logger("PNR retrieved from Queue and SWS PNR are different")     
                        print("PNR retrieved from Queue and SWS PNR are different")
                        Logging.logger("QueuePNR - "+ HostPNR +" , SWSPNR - " + SWSRecievedPNR)
                        print("QueuePNR - "+ HostPNR +" , "  "SWSPNR - " + SWSRecievedPNR)
                    else:
                        Logging.logger("PNR processed earlier is same as current one")
                        print("PNR processed earlier is same as current one")
                        Logging.logger("EalierPNR - "+ HostPNR + " , CurrentPNR - "+ HostPNR)
                        print("EalierPNR - "+ HostPNR + " , CurrentPNR - "+ HostPNR)
                    Logging.logger("Ignoring the PNR - I")
                    print("Ignoring the PNR - I")
                    HostCommand = "I"
                    Ignore_Response = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
                    Ignore_resStart = Ignore_Response.find("<Response>") + 10
                    Ignore_resEnd = Ignore_Response.find("</Response>")
                    Ignore_Response = Ignore_Response[Ignore_resStart:Ignore_resEnd]
                    Logging.logger(Ignore_Response)
                    print(Ignore_Response)

                    if tryAgainFlag == '':
                        tryAgainFlag = "Y"
                        Logging.logger("Ignored the PNR to process Next one if present")
                        print("Ignored the PNR to process Next one if present")
                        finish_flag = OPA_checkQueue.check_queue(Pcc, Ignore_Response, g_pnrHold, tryAgainFlag, QueueNo, BinaryToken, finish_flag, notsignIn_flag, ticketingLimitFixAttemptFlag, db_conn)
                    else:
                        if tryAgainFlag == "Y":
                            tryAgainFlag = ''
                            HostCommand = "QXI"
                            Logging.logger(HostCommand)
                            print(HostCommand)
                            ExitQueue = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
                            # ExitQueue_resStart = ExitQueue.find("<Response>") + 10
                            # ExitQueue_resEnd = ExitQueue.find("</Response>")
                            # ExitQueue = ExitQueue[ExitQueue_resStart:ExitQueue_resEnd]
                            ExitQueue = OPA_retrieveResponse.Response_Block(ExitQueue,10)
                            Logging.logger(ExitQueue)
                            print(ExitQueue)
                            Logging.logger("Exiting the Queue to attempt after Snooze")
                            print("Exiting the Queue to attempt after Snooze")
                            finish_flag = OPA_finishProcess.finish_process(QueueNo)

            if finish_flag=='0':
                tryAgainFlag = ''
                g_pnrHold = SWSRecievedPNR

        return SWSRecievedPNR, GetReservation_Response, g_pnrHold, tryAgainFlag, finish_flag