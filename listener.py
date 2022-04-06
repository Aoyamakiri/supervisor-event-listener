import sys
from timer_thread import TimerThread
from global_variable_pool import data_buffer, thread_lock


class Listener:
    READY = 'READY\n'
    RESULT = 'RESULT '

    def __init__(self) -> None:
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def ready(self) -> None:
        self.stdout.write(self.READY)
        self.stdout.flush()

    def success(self) -> None:
        self.stdout_send('OK')

    def fail(self) -> None:
        self.stdout_send('FAIL')

    def stdout_send(self, send_data) -> None:
        result_length = len(send_data)
        result = '%s%s\n%s' % (self.RESULT, str(result_length), send_data)
        self.stdout.write(result)
        self.stdout.flush()

    def run(self) -> None:
        while True:
            self.ready()

            line = self.stdin.readline()
            header = dict([x.split(':') for x in line.split()])
            payload = self.stdin.read(int(header['len']))

            thread_lock.acquire()
            data_buffer.append({'header': header, 'payload': payload})
            thread_lock.release()

            self.success()


if __name__ == '__main__':
    delay = 60  # 延迟多少秒后发送
    config = {
        'smtp_server': '',  # 邮件服务器域名
        'smtp_port': 465,  # 邮件服务器端口
        'smtp_username': '',  # 邮件服务器用户名
        'smtp_password': '',  # 邮件服务器密码

        'subject': '进程状态通知',  # 邮件主题
        'from_nickname': '',  # 发送者昵称
        'from_addr': '',  # 发送者地址
        'to_nickname': '',  # 接收者昵称
        'to_addr': '',  # 接收者地址
    }

    timer_thread = TimerThread(1, 'timer', delay, config)
    timer_thread.setDaemon(True)
    timer_thread.start()
    listener = Listener()
    listener.run()
