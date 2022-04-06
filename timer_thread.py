from email import header
import time
import threading
from mail import Mail
from data_processing import *
from global_variable_pool import data_buffer, thread_lock


class TimerThread (threading.Thread):
    def __init__(self, thread_id, name, delay, config) -> None:
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.delay = delay
        self.last_time = int(time.time())
        self.config = config

    def run(self) -> None:
        while True:
            time.sleep(1)
            now_time = int(time.time())
            if now_time - self.last_time >= self.delay:
                send_message_finally = ''
                thread_lock.acquire()

                for i in range(len(data_buffer)):
                    explanation = processing_header(data_buffer[i]['header'])
                    message = processing_payload(data_buffer[i]['payload'])
                    split_line = ''
                    if i != len(data_buffer) - 1:
                        split_line = '-------------------------------------------------------------\n\n'
                    send_message = message + '\n\n说明: ' + explanation + '\n\n' + split_line
                    send_message_finally += send_message

                if data_buffer:
                    mail = Mail(self.config)
                    mail.send(send_message_finally)

                data_buffer.clear()
                thread_lock.release()
                self.last_time = now_time
