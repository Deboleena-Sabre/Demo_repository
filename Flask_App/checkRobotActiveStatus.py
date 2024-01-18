import datetime
import SendEmail
import mysql.connector
from datetime import datetime
import time
import Logging




def checkRobotStatus():

    inactive_mailSent = 'N'
    mydb = mysql.connector.connect(
        host="17.129.253.37",
        user="parameswaran",
        password="Sundaramoorthyd8de",
        database="dev"
        )

    # mycursor1 = mydb.cursor()
    while(True):

        mydb.commit()
        mycursor1 = mydb.cursor()
        
        Logging.roboCheckLogger("Checking for last active time")
        print("Checking for last active time")


        current_time=datetime.now()
        query = "select LastActiveDateTime from irobo_copy" + " where UserID="+'"9984"'+" and AppName="+'"ApprovalRobot"'

        Logging.roboCheckLogger("Current Query : " + query)
        print("Current Query : " + query)

        mycursor1.execute(query)
        last_active_time=mycursor1.fetchall()
        last_activity_time=last_active_time[0][0]

        Logging.roboCheckLogger("Current Data fetched : " + str(last_activity_time))
        print("Current Dtaa fetched : " + str(last_activity_time))

        print("current time = " + str(current_time))
        print("Last_active_time = " + str(last_activity_time))

        duration = current_time - last_activity_time    

        print("Curr-last = " + str(duration))                 
        duration_in_s = duration.total_seconds()

        print("Duration in seconds = " + str(duration_in_s))
        minutes = duration_in_s/60

        print("Minutes = " + str(minutes))
        if minutes>0.5 and inactive_mailSent!= 'Y':
            Logging.roboCheckLogger("Robot inactive.....sending mail")
            print("Robot inactive.....sending mail")
            SendEmail.send_mail()
            Logging.roboCheckLogger("Mail Sent")
            print("Mail Sent")
            inactive_mailSent = 'Y'
            #what to do after sending mail

        elif(minutes>0.5 and inactive_mailSent=='Y'):
            Logging.roboCheckLogger("Robot is inactive....already sent mail to the admin")
            print("Robot is inactive....already sent mail to the admin")

        else:
            Logging.roboCheckLogger("Robot is active")
            print("Robot is active")

        time.sleep(20)
