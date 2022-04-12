import requests
import json
import smtplib
import os

SEND_EMAIL = os.environ.get('GEAR_EMAIL')
SEND_PASS = os.environ.get('GEAR_PASS')


def success_email(payload):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(SEND_EMAIL, SEND_PASS)

        order_number = payload['order']['number']
        creation = payload['order']['createdAt']

        subject = f'{order_number} Successfully Uploaded'
        body =f'{order_number} was uploaded at {creation}'
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(SEND_EMAIL, SEND_EMAIL, msg)

def return_json(payload, url):
    return requests.post(url, data=json.dumps(payload),  headers={'Content-Type': 'application/json'})