import sqlite3
import pandas as pd

# Connect to SQLite
connection = sqlite3.connect("titanic.db")

# Create a cursor object to insert records and create table
cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE PASSENGER(
    PassengerId INT,
    Survived INT,
    Pclass INT,
    Name TEXT,
    Sex TEXT,
    Age REAL,
    SibSp INT,
    Parch INT,
    Ticket TEXT,
    Fare REAL,
    Cabin TEXT,
    Embarked TEXT
);
"""
cursor.execute(table_info)

# Load Titanic dataset
titanic_data = pd.read_csv("titanic.csv")

# Insert records into the database
for index, row in titanic_data.iterrows():
    cursor.execute('''INSERT INTO PASSENGER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        row['PassengerId'],
        row['Survived'],
        row['Pclass'],
        row['Name'],
        row['Sex'],
        row['Age'],
        row['SibSp'],
        row['Parch'],
        row['Ticket'],
        row['Fare'],
        row['Cabin'],
        row['Embarked']
    ))

# Display all the records
print("The inserted records are:")
data = cursor.execute('''SELECT * FROM PASSENGER LIMIT 5''')
for row in data:
    print(row)

# Commit your changes to the database
connection.commit()
connection.close()
