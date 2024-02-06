from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import pandas as pd

import google.generativeai as genai

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(sql, conn)  # Read SQL query directly into DataFrame
    conn.close()
    return df

# Define Your Prompt
prompt = ["""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name PASSENGER and has the following columns - PassengerId, Survived,
    Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked\n\nFor example,\nExample 1 - How many passengers survived?,
    the SQL command will be something like this SELECT COUNT(*) FROM PASSENGER WHERE Survived = 1;
    \nExample 2 - Show details of passengers who paid fare more than 100?,
    the SQL command will be something like this SELECT * FROM PASSENGER WHERE Fare > 100;
    also the sql code should not have ``` in beginning or end and sql word in output
"""]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Titanic Dataset Information")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response_df = read_sql_query(response, "titanic.db")
    st.subheader("The Response is")
    st.write(response_df)
