from datetime import datetime

def logger(log_status):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d%b%y")
    # logFileProcess = "/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"
    logFileProcess = "/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"
    f = open(logFileProcess, "a",encoding="utf-8")
    f.write(current_time+"  "+log_status+"\n")
    f.close
    # print(log_status)


def roboCheckLogger(log_status):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d%b%y")
    logFileiRobo = "/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/ApprovalRobot_OPA_iRoboLog__" + current_date + ".txt"
    f = open(logFileiRobo, "a",encoding="utf-8")
    f.write(current_time+"  "+log_status+"\n")
    f.close
    # print(log_status)


def OPASWSLogger(log_status, SWSCallType):
    now = datetime.now()
    timeStamp = now.strftime("%Y/%m/%d %H:%M:%S")
    current_date = now.strftime("%d%b%y")
    logFileSWS = "/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/ApprovalRobot_OPA_SWSLog__" + current_date + ".txt"
    f = open(logFileSWS, "a",encoding="utf-8")

    
    f.write(str(timeStamp) + " - "+ "[SWS.QIK.DEBUG.LOG]:"+ SWSCallType+"::, ")
    f.write(log_status + "\n")

    if(SWSCallType=='RESPONSE'):
        f.write("------------------------------------------------------------------------------------------------------------------------------------------"+"\n")
    

    f.close()


def ATPLogger(log_status,ATPCallType):
    now = datetime.now()
    timeStamp = now.strftime("%Y/%m/%d %H:%M:%S")
    current_date = now.strftime("%d%b%y")
    logFileATP = "/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/ApprovalRobot_OPA_ATPLog__" + current_date + ".txt"
    f = open(logFileATP, "a",encoding="utf-8")    
    f.write(str(timeStamp) + " - "+ "[ATP.QIK.DEBUG.LOG]:"+ ATPCallType+":: ")
    f.write(str(log_status) + "\n")
    if(ATPCallType=='RESPONSE'):
        f.write("------------------------------------------------------------------------------------------------------------------------------------------"+"\n")
    f.close()
