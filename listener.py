import sys
from mail import Mail

global headers, data


class Listener:
    def __init__(self) -> None:
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def success(self) -> None:
        self.stdout.write('RESULT 2\nOK')
        self.stdout.flush()

    def fail(self) -> None:
        self.stdout.write('RESULT 4\nFAIL')
        self.stdout.flush()

    def run(self, callback) -> None:
        global headers, data
        while True:
            self.stdout.write('READY\n')
            self.stdout.flush()

            line = self.stdin.readline()
            headers = dict([x.split(':') for x in line.split()])
            data = self.stdin.read(int(headers['len']))

            try:
                callback()
                self.success()
            except:
                self.fail()


if __name__ == '__main__':
    def logic():
        global headers, data
        # TODO
        config = {
            'smtp_server': '', # 邮件服务器域名
            'smtp_port': 465, # 邮件服务器端口
            'smtp_username': '', # 邮件服务器用户名
            'smtp_password': '', # 邮件服务器密码

            'subject': '进程状态更改', # 邮件主题
            'from_nickname': '', # 发送者昵称
            'from_addr': '', # 发送者地址
            'to_nickname': '', # 接收者昵称
            'to_addr': '', # 接收者地址
        }

        event_name = headers['eventname']
        if event_name == 'PROCESS_STATE_EXITED':  # 进程已从RUNNING状态转移到EXITED状态 即被kill
            config['subject'] = '进程终止'
            explanation = '进程已从 「正在运行」 状态转移到 「退出」 状态'
        elif event_name == 'PROCESS_STATE_STARTING':  # 进程已转移到STARTING状态
            config['subject'] = '进程正在启动'
            explanation = '进程已从之前的任何状态转移到 「正在启动」 状态'
        elif event_name == 'PROCESS_STATE_RUNNING':  # 进程已从STARTING状态转移到RUNNING状态 即成功启动
            config['subject'] = '进程启动成功'
            explanation = '进程已从 「正在启动」 状态转移到 「启动完成」 状态'
        elif event_name == 'PROCESS_STATE_BACKOFF':  # 进程已从STARTING状态转移到BACKOFF状态
            config['subject'] = '进程启动失败'
            explanation = '进程已从 「正在启动」 状态转移到 「启动失败」 状态'
        elif event_name == 'PROCESS_STATE_FATAL':  # 进程已从BACKOFF状态移动到FATAL状态 即多次未成功启动进程 并放弃尝试重新启动它
            config['subject'] = '进程无法启动'
            explanation = '进程多次未能成功启动 已放弃尝试重新启动它'
        else:
            explanation = '事件名称: ' + event_name

        mail = Mail(config)
        mail.send(data, explanation)

    listener = Listener()
    listener.run(logic)
