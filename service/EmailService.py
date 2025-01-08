import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dto.OTPMail import getotpMail, getpassresetmail
from service.OTPService import generateotp
from dto.WaitlistMail import getwaitlistmail
from database.databaseConfig.databaseConfig import SessionLocal
from database.entity.Email import Email
from typing import Optional

sender_email = 'noreply@websparks.ai'
sender_password = 'ay?xbL7u'
mailserver = "smtp.zoho.com"

def send_OTPBYemail(recipient_email: str, subject: str, userid: int, username: Optional[str] = ''):
    # Set up the MIME
    
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    mail_content = getotpMail(generateotp(userid=userid), username=username)
    msg.attach(MIMEText(mail_content, 'html'))

    # Add body to email
    #msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL(mailserver, 465)
        #server.starttls()

        # Login to your email account
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        
def send_passresetMail(recipient_email: str, subject: str, userid:int ) -> bool:
    # Set up the MIME

    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    mail_content = getpassresetmail(generateotp(userid=userid))
    msg.attach(MIMEText(mail_content, 'html'))

    # Add body to email
    #msg.attach(MIMEText(message, 'plain'))
    

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL(mailserver, 465)
        #server.starttls()

        # Login to your email account
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        return False
    
    
def send_waitlistmail(recipient_email: str, subject: str, name: str ) -> bool:
    # Set up the MIME
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    mail_content = getwaitlistmail(name=name)
    msg.attach(MIMEText(mail_content, 'html'))

    # Add body to email
    #msg.attach(MIMEText(message, 'plain'))
    

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL(mailserver, 465)
        #server.starttls()

        # Login to your email account
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        return False
    
    
def send_Email(requestmail: str, name: str, message: str) -> bool:
    # Set up the MIME

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
    msg['Subject'] = 'User Email test'
    msg.attach(MIMEText('Email from '+name+' User email '+requestmail+' message '+message, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL(mailserver, 465)
        # server.starttls()

        # Login to your email account
        print(server.login(sender_email, sender_password))

        # Send email
        print(server.sendmail(sender_email, requestmail, msg.as_string()))
        server.quit()
        print('email sent')
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        return False
    
def send_user_Email(requestmail: str, subject: str, message: str, usermail: str) -> bool:

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = usermail
    msg['Subject'] = 'User Email '+subject
    msg.attach(MIMEText('Email from '+requestmail+' subject '+subject+' message '+message, 'plain'))
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP_SSL(mailserver, 465)
        # server.starttls()
        # Login to your email account
        server.login(sender_email, sender_password)
        # Send email
        server.sendmail(sender_email, sender_email, msg.as_string())
        server.quit()
        session = SessionLocal()
        session.add(Email(send_Email, usermail, "User Email", msg.as_string()))
        session.commit()
        session.flush()
        session.close()
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        return False



