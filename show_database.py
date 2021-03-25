import pandas as pd
import pymongo
import streamlit as st


def connect_to_registration_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.get_database('registration')
    records = db.register
    all_records_df = pd.DataFrame.from_records(records.find())
    return all_records_df

st.title("View Database")

db_option = st.radio(
    "Which database do you want to view?",
    ('Registration-DB', 'Visitor-DB'))

if db_option == 'Registration-DB':
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.get_database('registration')
    records = db.register
    all_records_df = pd.DataFrame.from_records(records.find())
    st.dataframe(all_records_df)  
    

else:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    visitor = client.get_database('visitor')
    visit_records = visitor.register
    visitor_df = pd.DataFrame.from_records(visit_records.find())
    st.dataframe(visitor_df)