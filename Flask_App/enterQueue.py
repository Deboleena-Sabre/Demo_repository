import Logging
import SendSabreCommand



def EnterQueue(Pcc, QueueNo, BinaryToken):
    Logging.logger("Accessing Queue for Next PNR")
    HostCommand = "q/"+Pcc+QueueNo
    Logging.logger(HostCommand)
    QueueResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
    Queue_resStart = QueueResponse.find("<Response>") + 10
    Queue_resEnd = QueueResponse.find("</Response>")
    QueueResult = QueueResponse[Queue_resStart:Queue_resEnd]


    return QueueResult

    