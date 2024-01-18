import OPA_getDBConnection
import OPA_updateFiles
import time
from datetime import datetime
import OPAMain_OverPcc

def checkForUpdates():
    mycursor = OPA_getDBConnection.DBConnection()
    query = "Select UpdatesAvailableFlag from irobo" + " where UserID="+'"9984"'+" and AppName="+'"ApprovalRobot"'
    count = 0
    while(True):
        midNightTimeFlag = 'N'
        currentTime = datetime.now()
        currentTime = currentTime.strftime("%H")
        currTime = int(currentTime)

        if(currTime>=23 and currTime<1):
            midNightTimeFlag = 'Y'
            updateAvailableFlag = 'Y'
        elif currTime>=1:
            count = 0

        mycursor.execute(query)
        myresult = mycursor.fetchall()
        updateAvailableFlag = myresult[0][0]
        if(updateAvailableFlag == 'Y' ):
            if(midNightTimeFlag=='Y' and count<1):
                OPA_updateFiles.updateFiles()
                count = count+1
                OPAMain_OverPcc.OverPcc()        #restart the robot
                
            elif(midNightTimeFlag == 'Y' and count>=1):
                continue           
            else:
                OPA_updateFiles.updateFiles()
                OPAMain_OverPcc.OverPcc()         #restart the robot

            updateAvailableFlag = 'N'
            midNightTimeFlag = 'N'
            query ="Update irobo set UpdatesAvailableFlag="+'"N"'+" where UserID="+'"9984"'+" and AppName="+'"ApprovalRobot"'
            mycursor.execute(query)
            mycursor.execute('COMMIT')

        time.sleep(1800)
    