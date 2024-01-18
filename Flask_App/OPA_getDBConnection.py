# import mysql.connector

import mysql.connector as connector


def DBConnection():
    # Database connection
    # mydb = mysql.connector.connect(
    # host="17.129.253.37",
    # user="parameswaran",
    # password="Sundaramoorthyd8de",
    # database="dev"
    # )

    # print(mydb)
    # mycursor = mydb.cursor()
    
    # return mycursor

    config = {
        "user": "parameswaran",
        "password": "Sundaramoorthyd8de",
        "host": "17.129.253.37",
        "database": "dev"
    }
    try:
        c = connector.connect(**config)
    except:
        print("connection error")
        exit(1)


    mycursor = c.cursor()
    return mycursor