import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()
sender_email = os.getenv('sender_email')
sender_password = os.getenv('sender_password') # app password through gmail "create and use app passwords": https://support.google.com/mail/answer/185833?hl=en

print(sender_email)
print(sender_password)

def send_email(personal_template, email):
    """ personal_template: string that contains email body
        email: string 
    """
    recipient_email = email
    email_subject = 'Sponsorship for Indigenous Engagement in STEAM'
    email_body = personal_template

    msg = MIMEMultipart()
    msg['Subject'] = email_subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    msg.attach(MIMEText(email_body, 'html'))

    # attaches the pdf package to the email
    with open('CISSA Sponsorship Package 2023-2024.pdf', 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream') 
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= CISSA Sponsorship Package 2023-2024.pdf",
    )

    msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())


# company name and emails csv into pandas dataframe
company_info_path = 'test_email_list.csv'
company_info_df = pd.read_csv(company_info_path)

# takes email body from a text file and reads
email_body_path = 'body.txt'
with open(email_body_path, 'r') as email_body:
    email_template = email_body.read()

# goes through each company and email 
for index, row in company_info_df.iterrows():
    company = row['company']
    email = row['email']
    # replaces [Company name] with personalized name
    personal_template = email_template.replace('[Company Name]', company)
    body_html = f"""
    <html>
        <body>
            {personal_template}
        </body>
    </html>
    """
    print(email) # to know which emails sent
    # print(personal_template)
    send_email(personal_template, email) # ONLY WHEN READY (keep our emails to know if it sent at beginning and end)


