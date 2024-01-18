from tkinter import *
import time
import threading
import OPAMain_OverPcc
from datetime import datetime

now = datetime.now()
current_date = now.strftime("%d%b%y")
logFileProcess = "ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"
logFileiRobo = "ApprovalRobot_OPA_iRoboLog__" + current_date + ".txt"
f1 = open("/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/"+logFileProcess, "a")
f2 = open("/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/"+logFileiRobo, "a")
f1.close
f2.close

thread = threading.Thread(target = OPAMain_OverPcc.OverPcc, args=[])
thread.start()



# logFileProcess = "ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"

def update_a(f_a,display_a): 
    data = f_a.read()
    f_a.readlines()
    display_a.insert(END,data)
    display_a.see("end")
    # time.sleep(2)
    display_a.after(1000,lambda:update_a(f_a,display_a))
def update_b(f_b,display_b):   
    data = f_b.read()
    f_b.readlines()
    display_b.insert(END,data)
    display_b.see("end")
    # time.sleep(2)
    display_b.after(1000,lambda:update_b(f_b,display_b))


def display_file(file_name_a,file_name_b):
    root = Tk()     
    # root.geometry("1200x600") 
    # root.maxsize("1200x600") 
    display_a = Text(root,height = 65,width = 100,highlightthickness=0, borderwidth=1, padx=5,pady = 10, font=("Monospaced",10),fg="black", bg="white")
    display_b = Text(root,height = 65,width = 100,highlightthickness=0, borderwidth=1, padx=10,pady = 10, font=("Monospaced",10),fg="white", bg="black")
    display_a.grid(column=0,row=0)  #,ipadx=0,padx=0,sticky=E+W)
    display_b.grid(column=1,row=0)  #,ipadx=0,padx=0,sticky=E+W)
    scrollbar = Scrollbar()
    # scrollbar.pack(side='
    scrollbar.grid(row=0, column=2, sticky=NS)
    display_a['yscrollcommand'] = scrollbar.set
    display_b['yscrollcommand'] = scrollbar.set
    scrollbar['command'] = display_a.yview
    scrollbar['command'] = display_b.yview
    f_a=open(file_name_a,'r')
    f_b=open(file_name_b,'r')
    # def display_log(file,display_window):
    #     if display_window ==display_a:
    #         f_a=open(file,'r')
    #         update_a()
    #     else:
    #         f_b=open(file,'r')
    #         update_b()
    update_a(f_a,display_a)
    update_b(f_b,display_b)

    root.resizable(True, True)  # This code helps to disable windows from resizing

    window_height = 800
    window_width = 1500

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    root.eval('tk::PlaceWindow . center')

    root.title('Log Window')
    root.mainloop()



display_file('/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/'+logFileiRobo,'/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/'+logFileProcess)



# import tkinter as tk 
# import time
# import call_display_log
# import threading
# import OPAMain_OverPcc

# thread = threading.Thread(target = OPAMain_OverPcc.OverPcc, args=[])
# thread.start()

# def run(text, openFile):
#     data = openFile.read()
#     openFile.readlines()
#     text.insert('end', data)
#     text.see("end")
#     # time.sleep(1)
#     text.after(500, lambda: run(text, openFile))
# def window(file="ApprovalRobot_OPA_iRoboLog__04Jan23.txt"):
#     root = tk.Tk()
#     # print(file)
#     text = tk.Text(pady=5, padx=5,bg="black",fg="white")
#     text.pack(side='left', fill='both', expand=True)
#     scrollbar = tk.Scrollbar()
#     scrollbar.pack(side='right', fill='y')
#     text['yscrollcommand'] = scrollbar.set
#     scrollbar['command'] = text.yview
#     openFile = open(file, 'r')
#     run(text, openFile)
#     root.mainloop()


# window()
