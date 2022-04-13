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
