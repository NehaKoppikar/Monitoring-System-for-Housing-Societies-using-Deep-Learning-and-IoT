import sendgrid
from sendgrid.helpers.mail import Mail
import schedule
import time
from creds import key, from_email, to_email
import datetime
import pandas as pd
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
visitor = client.get_database('visitor')
visit_records = visitor.register
visitor_df = pd.DataFrame.from_records(visit_records.find())

message = Mail(
    from_email=from_email,
    to_emails=to_email,
    subject='Daily Visitor Report',
    html_content=visitor_df.to_html())
try:
    sg = sendgrid.SendGridAPIClient(api_key=key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))


# sg = sendgrid.SendGridAPIClient(api_key=key)
# data = {
#     "personalizations": [
#         {
#             "to": [
#                 {
#                     "email": to_email
#                 }
#             ],
#             #"send_at": 1600188812,
#             "subject": "Daily Visitor Report"
#         }
#     ],
#     "from": {
#         "email": from_email
#     },
#     "content": [
#         {
#             "type": "table",
#             "value": visitor_df.to_html()
#         }
#     ]
# }

# def send_email():
#     response = sg.client.mail.send.post(request_body=data)

# response = sg.client.mail.send.post(request_body=data)
# print(response.status_code)
# print(response.body)
# print(response.headers)

#schedule.every().day.at("05:08").do(send_email)

# yesterday = (datetime.datetime.today() - timedelta(days=1)).strftime("%d %B, %Y")

# while True:
#     schedule.run_pending()
#     time.sleep(2)

# using SendGrid's Python Library
# # https://github.com/sendgrid/sendgrid-python
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='neha.koppikar1721@nmims.edu.in',
#     to_emails='neha.koppikar1721@nmims.edu.in',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     #sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     sg = SendGridAPIClient("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")
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)