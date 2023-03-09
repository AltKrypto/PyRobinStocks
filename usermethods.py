import os
from dotenvy import load_env, read_file
import pyotp
import robin_stocks.robinhood as rh
from datetime import date
import csv
import sqlite3 as sq
import pandas as pd

#
#             STANDARD FUNCTIONS
#

def login():
    # Handles logging in to the Robinhood API
    load_env(read_file('.env'))
    user = os.environ.get('username')
    passw = os.environ.get('password')
    auth = os.environ.get('auth')
    totp = pyotp.TOTP(auth).now()
    login = rh.login(user, passw, mfa_code = totp)
    
def cleanUp():
    # Closes the current and purges all previous sessions
    rh.logout
    purge = os.listdir('.tokens')
    for i in purge:
        os.remove(f'.tokens/{i}')
    print('You have been logged out and all sessions have been purged!')

def dividends():
    # Returns todays date and the total dividends paid
    today = str(date.today())
    divi = round(rh.account.get_total_dividends(), 2)
    print(f'As of {today} you have made {divi} in dividends')
    return [today, divi]

def account():
    # Returns basic Robinhood account information
    account = rh.build_user_profile()
    return account
    
def holdings():
    # Returns a raw collection of dicts for all positions
    print('Loading your positions.....')
    print('Please be patient, this may take several minutes.')
    positions = rh.build_holdings()
    return positions
    
def divTrackCsv():
    # Exports position data to csv for importing into DivTracker
    tickers =[]
    resolved = []
    field_names = ['Ticker', 'Quantity', 'Cost Per Share', 'Date']
    today = str(date.today())
    pos = holdings()
    for i in pos.keys():
        tickers.append(i)
        tickers.sort()
    for i in tickers:
        ticker = i
        shares = (pos[i]['quantity'])
        cost = (pos[i]['average_buy_price'])
        itter = {'Ticker': ticker, 'Quantity': shares, 'Cost Per Share': cost, 'Date': today}
        resolved.append(itter)
    print('Generating CSV')
    with open('positions.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(resolved)
    print('File exported as positions.csv')
    
    
#
#           DATABASE MANIPLUATION
#

    
    def tickerTable():
    # create and connect to database
    connection = sq.connect('test.db')
    curs = connection.cursor()
    # creates a table for storing ticker names
    curs.execute("create table if not exists tickers" + " (ticker text)")
    # reads the ticker names from positions and outputs them as a column in the "tickers" table in the "positions" database
    data = pd.read_csv('positions.csv', usecols=['Ticker'])
    data.to_sql('tickers', connection, if_exists='replace', index=True)
    # select all the records
    curs.execute('select * from tickers')
    # fetch the records that were selected
    records = curs.fetchall()
    for row in records:
    	print(row)
    # close the database
    connection.close()
    
