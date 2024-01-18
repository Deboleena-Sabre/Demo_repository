# from OPARobotMain import BinaryToken
import SendSabreCommand 
import Logging

def checkQueue(response_check,QueueNo,BinaryToken):
    Empty_Queue = ''
    Emp_check = response_check.find("END OF DISPLAY FOR REQUESTED DATA")
    if Emp_check != -1:
        Empty_Queue = "Y"
    Emp_check = response_check.find("QUEUE SELECTED WAS EMPTY")
    if Emp_check != -1:
        Empty_Queue = "Y"
    Emp_check = response_check.find("QUEUE EMPTY")
    if Emp_check != -1:
        Empty_Queue = "Y"
    Emp_check = response_check.find("NOTHING ON QUEUE")
    if Emp_check != -1:
        Empty_Queue = "Y"
    Emp_check = response_check.find(" NO PNRS ON Q")
    if Emp_check != -1:
        Empty_Queue = "Y"
    Emp_check = response_check.find("CANNOT DO THIS IF ON QUEUE")
    if Emp_check != -1:
        HostCommand = "QXI"
        RecievedResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        Logging.logger(RecievedResponse)
        checkQueue(response_check,QueueNo)
    Emp_check = response_check.find("FIN OR IG")
    if Emp_check != -1:
        HostCommand = "I"
        RecievedResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        Logging.logger(RecievedResponse) 
        HostCommand = "QXI"
        RecievedResponse = SendSabreCommand.SendSabreAPI(BinaryToken,HostCommand)
        Logging.logger(RecievedResponse)    
        checkQueue(response_check,QueueNo)
        
    Emp_check = response_check.find("NO PNRS FOUND ON QUEUE")
    if Emp_check != -1:
        Empty_Queue = "Y"    


    if QueueNo != '':
        if Empty_Queue == "Y":
            Logging.logger("Queue "+QueueNo+ " is currently empty")
            print("Queue "+QueueNo+ " is currently empty")

    return Empty_Queue


