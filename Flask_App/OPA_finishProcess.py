
import Logging

def finish_process(QueueNo, finish_flag):
    finish_flag = '1'
    Logging.logger("END OF PROCESS FOR QUEUE - "+QueueNo)
    print("END OF PROCESS FOR QUEUE - "+QueueNo)

    return finish_flag

