import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = "test8318327@gmail.com"
password = "test1234@"

def send_mail(text="Email body", subject="Hello World", from_email="Test Test <test8318327@gmail.com>", to_emails=None, html=None):
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    
    txt_parts = MIMEText(text, 'plain')
    msg.attach(txt_parts)
    if html != None:
        html_parts = MIMEText(text, 'html')
        msg.attach(html_parts)
    
    msg_str = msg.as_string()
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()