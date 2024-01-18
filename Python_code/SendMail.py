import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_mail():

    msg = EmailMessage()
    msg.set_content("""
    Hello,
    Changes in app files updated successfully!
    """)

    msg['Subject'] = 'Update Status'
    msg['From'] = "mailtesting415@gmail.com"
    msg['To'] = "shiveshchaturvedi38@gmail.com"

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("mailtesting415@gmail.com", "axcmaxnxqhapqsxt")
    server.send_message(msg)
    server.quit()