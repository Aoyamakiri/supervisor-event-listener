import time
import string
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail:
    def __init__(self, config) -> None:
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.smtp_username = config['smtp_username']
        self.smtp_password = config['smtp_password']

        self.subject = config['subject']
        self.from_nickname = config['from_nickname']
        self.from_addr = config['from_addr']
        self.to_nickname = config['to_nickname']
        self.to_addr = config['to_addr']

        self.smtp = smtplib.SMTP_SSL()
        self.smtp.connect(self.smtp_server, self.smtp_port)
        self.smtp.login(self.smtp_username, self.smtp_password)

    def format_data(self, data) -> string:
        try:
            data = data.split(' ')
            processname = data[0].split(':')[1]
            groupname = data[1].split(':')[1]
            from_state = data[2].split(':')[1]
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            return '进程名: ' + processname + '\n进程组名: ' + groupname + '\n当前进程状态: ' + from_state + '\n时间: ' + now
        except:
            return data

    def send(self, data, explanation=None, is_format_data=True) -> None:
        if is_format_data is True:
            data = self.format_data(data)

        if explanation is not None:
            data = data + '\n\n说明: ' + explanation

        message = MIMEText(data, 'plain', 'utf-8')
        message['Subject'] = self.subject
        message['From'] = formataddr([self.from_nickname, self.from_addr])
        message['To'] = formataddr([self.to_nickname, self.to_addr])

        self.smtp.sendmail(self.from_addr, self.to_addr, message.as_string())
        self.smtp.quit()
