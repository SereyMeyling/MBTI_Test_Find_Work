import smtplib
from email.mime.text import MIMEText

def send_email(name,email,message,subject):
    port=2525
    smtp_server = 'smtp.mailtrap.io'
    login = '050475161a7ab7'
    password = '942a39eca04c73'

    sender_email= email
    receiver_email= 'mbtifindyourcarrer@gmail.com'
    msg=MIMEText(message,'html')
    msg['Subject']=subject+" from "+name
    msg['From']=sender_email
    msg['To']=receiver_email

    with smtplib.SMTP(smtp_server,port) as server:
        server.login(login,password)
        server.sendmail(sender_email,receiver_email,msg.as_string()) 