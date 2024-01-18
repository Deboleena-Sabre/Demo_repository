from flask import Flask, render_template
import datetime 
import time
import threading
import OPAMain_OverPcc
from datetime import datetime
from flask import Response


# from loguru import logger


# configure logger
# logger.add("app/static/job.log", format="{time} - {message}")



APP = Flask(__name__, static_folder="app/static/", template_folder="app/static/")
@APP.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")

def send_response(joblog,joblog1):
    log_a=joblog
    log_b=joblog1
    while True:
        val = log_a.read()
        val2 = log_b.read()
        yield val
        time.sleep(1)
        yield val2
        time.sleep(1)

def flask_logger(file1, file2):
    """creates logging information"""
    jobLog = open(file1, 'r')
    jobLog2 = open(file2, 'r')

    res=send_response(jobLog, jobLog2)
    # res1,res2=zip(*send_response(jobLog, jobLog2))
    # return res1,res2
    return next(res), next(res)
    
    
    # with open("app/static/job.log") as log_info:
    #     for i in range(25):
    #         logger.info(f"iteration #{i}")
    #         data = log_info.read()
    #         yield data.encode()
    #         time.sleep(1)
    #     # Create empty job.log, old logging will be deleted
    #     open("app/static/job.log", 'w').close()
    # """creates logging information"""
    # for i in range(100):
    #     current_time = datetime.datetime.now().strftime('%H:%M:%S') + "\n"
    #     yield current_time.encode()
    #     time.sleep(1)

def read_log_file(path: str):
    with open(path) as f:
            while True:
                yield f.read()
                time.sleep(1)

    # """ Yield each line from a file as they are written.
    # `sleep_sec` is the time to sleep after empty reads. """
    # line = ''
    # with open(path, 'r') as handle:
    #     while True:
            # tmp = handle.readline()
            # if tmp is not None:
            #     line += tmp
            #     if line.endswith("\n"):
            #         yield line
            #         line = ''

@APP.route("/log_stream_2", methods=["GET"])
def log_stream_1():
    """returns logging information"""
    now = datetime.now()
    current_date = now.strftime("%d%b%y")
    logFileProcess = "ApprovalRobot_OPA_ProcessLog__" + current_date + ".txt"
    logFile2 = r"/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/"+logFileProcess
    return server_logs(logFile2)

@APP.route("/log_stream_1", methods=["GET"])
def log_stream_2():
    """returns logging information"""
    thread = threading.Thread(target = OPAMain_OverPcc.OverPcc, args=[])
    thread.start()
    now = datetime.now()
    current_date = now.strftime("%d%b%y")
    logFileiRobo = "ApprovalRobot_OPA_iRoboLog__" + current_date + ".txt"
    logFile1 = r"/Users/ShubhamKhandelwal/Documents/OPA_Robot_working/logFiles/"+logFileiRobo
    return server_logs(logFile1)

def server_logs(path: str):
    return Response(read_log_file(path), mimetype="text/plain", content_type="text/event-stream")

if __name__ == "__main__":
    APP.run(host="127.0.0.1", port=8080, debug=True, threaded = True)