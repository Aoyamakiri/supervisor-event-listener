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

    def send(self, data) -> None:
        message = MIMEText(data, 'plain', 'utf-8')
        message['Subject'] = self.subject
        message['From'] = formataddr([self.from_nickname, self.from_addr])
        message['To'] = formataddr([self.to_nickname, self.to_addr])

        self.smtp.sendmail(self.from_addr, self.to_addr, message.as_string())
        self.smtp.quit()
