import sqlite3
from datetime import date
import csv

# testing
# takes the positions.csv output by the divTrackCsv function creates a database and parses the csv into a table called positions

# TODO:
# Needs modified to operate as a one to many database.
# Table 1 to hold the tickers
# Table 2 to hold shares, cost and date

today = str(date.today())

file = open('positions.csv', 'r')
data = list(csv.reader(file, delimiter = ','))
file.close()

# Connects to the database named if it exists, if not it is created then creates a cursur object named c
connection = sqlite3.connect("test.db")
c = connection.cursor()

# Creates a database table named positions with 4 colums named ticker, shares, cost and date
c.execute("CREATE TABLE positions (ticker TEXT, shares REAL, cost REAL, date TEXT)")

# Iterates through the csv file that was opened and passes the data into the database
c.executemany("""
    INSERT INTO positions ('ticker', 'shares', 'cost', 'date')
    VALUES (?, ?, ?, ?)""", data)
connection.commit()
connection.close()
