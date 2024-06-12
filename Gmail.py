import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class Email:
    def __init__(self):
        self.user = '2018182005@tukorea.ac.kr'
        self.pw = '!rlaehtjd1'

    def sendMail(self, logs, recvmail):
        to = recvmail
        subject = '텔레그램 코인 동향 전송'
        body = logs

        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = ", ".join(to)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'UTF-8'))

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.user, self.pw)
            server.sendmail(self.user, to, msg.as_string())
            server.close()

            return True
        except Exception as e:
            print('이메일을 보내는데 실패했습니다:', e)
            return False






