import threading
import time
from datetime import datetime
# from sqlalchemy import true
# import test
import Logging
# import Display_log

def calldisplay():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d%b%y")
    # fileName = "ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"
    fileName = "ApprovalRobot_OPA_iRoboLog__23Dec22.txt"

    # thread = threading.Thread(target = Display_log.window, args=[])
    # thread.start()
    i = 1
    while(i!=0):
        file = open(fileName, 'a')
        file.write(str(i)+'\n')
        file.close()
        print(i)
        i = i+1
        time.sleep(2)
