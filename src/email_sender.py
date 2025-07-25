
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(config, email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(config['smtp_host'], config['smtp_port'])
        server.starttls()
        server.login(config['smtp_user'], config['smtp_pass'])
        server.send_message(msg)
        server.quit()
        print("Email sent")
    except Exception as e:
        print(f"Failed to send - Error {e}")
