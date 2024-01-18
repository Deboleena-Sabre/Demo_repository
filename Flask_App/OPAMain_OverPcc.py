# pcc- vk87, 1i0g 
from ast import arg
import OPARobotMain
# import OPA_getDBConnection
from datetime import datetime
# import OPA_checkForUpdates
import time
import OPA_updateFiles
import Logging
import mysql.connector as connector
import checkRobotActiveStatus
import threading
# import Display_log
# import call_display_log

pcc = ['VK87', '1I0G']

config = {
        "user": "parameswaran",
        "password": "Sundaramoorthyd8de",
        "host": "17.129.253.37",
        "database": "dev"
    }
try:
    conn = connector.connect(**config)
except:
    print("connection error")
    exit(1)

#Deboleena comment
mycursor = conn.cursor()
# mycursor = OPA_getDBConnection.DBConnection()

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# current_date = now.strftime("%d%b%y")
# fileName = "ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"

# thread = threading.Thread(target = Display_log.window, args=[fileName])
# thread.start()

# thread = threading.Thread(target = call_display_log.calldisplay, args=[])
# thread.start()


thread = threading.Thread(target = checkRobotActiveStatus.checkRobotStatus,args= [])
thread.start()




def updateActiveDateTime():
    # mycursor = OPA_getDBConnection.DBConnection()
    currentTime = datetime.now()
    LastActiveDateTime = currentTime
    print("Lastactivetime = " + str(LastActiveDateTime))
    query ="Update irobo_copy set ActiveStatus="+'"Y"'+", LastActiveDateTime="+ "'" +str(LastActiveDateTime)+"'"+ " where UserID="+'"9984"'+" and AppName="+'"ApprovalRobot"'
    Logging.logger("Current Query : " + query)
    print("Current Query : " + query)
    mycursor.execute(query)
    mycursor.execute('COMMIT')
    Logging.logger("Database Updated")
    print("Database Updated")


def checkForUpdates():
    # mycursor = OPA_getDBConnection.DBConnection()
    query = "Select UpdatesAvailableFlag from irobo_copy" + " where UserID="+'"9984"'+" and AppName="+'"ApprovalRobot"'
    Logging.logger("Current Query : " + query)
    print("Current Query : " + query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    updateAvailableFlag = myresult[0][0]
    Logging.logger("Current Data Fetched : " + updateAvailableFlag)
    print("Current Data Fetched : " + updateAvailableFlag)
    return updateAvailableFlag

def OverPcc():

    # thread = threading.Thread(target = checkRobotActiveStatus.checkRobotStatus,args=[])
    # thread = threading.Thread(target = checkRobotActiveStatus.checkRobotStatus,args= (lambda : stop_thread, ))
    # thread.start()
    for i in pcc:
        
        updateActiveDateTime()

        OPARobotMain.OPARobotProcessing(i, conn)

        print("Queue "+ i + " got over")
        print("Updating active date time")
        updateActiveDateTime()
    
    updatesAvailableFlag = checkForUpdates()

    if(updatesAvailableFlag == 'Y'):
        OPA_updateFiles.updateFiles()
        Logging.logger("Update success...restarting the robot")
        print("Update Success....restarting the robot")

        query ="Update irobo_copy set UpdatesAvailableFlag="+'"N"'+ " where UserID="+'"9984"'+" and AppName="+'"ApprovalRobot"'
        Logging.logger("Current Query : " + query)
        print("Current Query : " + query)
        mycursor.execute(query)
        mycursor.execute('COMMIT')
        Logging.logger("Database Updated")
        print("Database Updated")
        
    else:
        Logging.logger("Robot Snooze for 10 seconds")
        print("Robot Snooze for 10 seconds")
        time.sleep(10)
        Logging.logger("Restarting the robot")
        print("Restarting the robot")


    OverPcc()




# OverPcc()




