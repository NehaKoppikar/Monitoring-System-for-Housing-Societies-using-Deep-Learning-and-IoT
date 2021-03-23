import pandas as pd
import pymongo
import streamlit as st


def connect_to_registration_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.get_database('registration')
    records = db.register
    all_records_df = pd.DataFrame.from_records(records.find())
    return all_records_df

db_option = st.radio(
    "Which database do you want to view?",
    ('Registration-DB', 'Visitor-DB'))

if db_option == 'Registration-DB':
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.get_database('registration')
    records = db.register
    all_records_df = pd.DataFrame.from_records(records.find())
    st.dataframe(all_records_df)  
    

# elif db_option == "Non-Resident":
#     st.write('You selected Non-Resident.')
else:
    st.write("You chose visitor data")