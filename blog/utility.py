import os
from email.message import EmailMessage
from .password import email_password
import ssl
import smtplib



def send_email(email_receiver,user_code):
    email_sender = 'shahranrifat2@gmail.com'
    subject = "Verification Code"
    body = "Verification Code:"+" "+user_code

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())