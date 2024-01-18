import smtplib
from email.message import EmailMessage
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_mail():
    msg = MIMEMultipart()
    msg['From'] = 'temeateam@apple.com'
    msg['To'] = 'skhandelwal2@apple.com'
    msg['Subject'] = 'Alert'
    message = 'Robot inactive'
    msg.attach(MIMEText(message))

    # mailserver = smtplib.SMTP('smtp.mail.me.com', 587)
    mailserver = smtplib.SMTP('mail.apple.com', 587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    # mailserver.login("nidhichhapolia17@icloud.com", "vimtxucohrhhsxhm")

    # mailserver.sendmail('nidhichhapolia17@icloud.com','deboleena.bhattacharyya@sabre.com',msg.as_string())
    mailserver.login("temeateam", "Travel123")

    mailserver.sendmail('temeateam@apple.com','skhandelwal2@apple.com',msg.as_string())

    mailserver.quit()

# send_mail()







# import smtplib
# from email.message import EmailMessage


# def send_mail():
#     msg = EmailMessage()
#     msg.set_content("""
#     Hello,
#     Robot is not working.Please check.
#     """)
#     msg['Subject'] = 'Update Status'
#     msg['From'] = "nchhapolia@apple.com"
#     msg['To'] = "shubham.khandelwal@sabre.com"

#     # Send the message via our own SMTP server.
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.login("mailtesting415@gmail.com", "axcmaxnxqhapqsxt")
#     # server = smtplib.SMTP_SSL('mail.apple.com', 993)
#     # server.login("temeateam", "Travel123")
#     server.send_message(msg)
#     server.quit()



