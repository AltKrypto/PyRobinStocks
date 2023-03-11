import os
from dotenvy import load_env, read_file
import pyotp
import robin_stocks.robinhood as rh
from datetime import date
import csv
import sqlite3 as sq
import pandas as pd

#
#             CONNECT TO LOCAL DATABASE
#

db_name = 'pyrobst.db'
connection = sq.connect(f'data/{db_name}')
curs = connection.cursor()
print('Connected to local database')

#
#             SESSION HANDLER
#


class Session():
  def login():
    # Handles logging in to the Robinhood API
    load_env(read_file('.env'))
    user = os.environ.get('username')
    passw = os.environ.get('password')
    auth = os.environ.get('auth')
    totp = pyotp.TOTP(auth).now()
    login = rh.login(user, passw, mfa_code=totp)

  def logout():
    # Closes the current and purges all previous sessions
    rh.logout
    purge = os.listdir('.tokens')
    for i in purge:
      os.remove(f'.tokens/{i}')
    connection.close
    print('Successfully logged out, database connection closed and all session history purged.')


#
#           SIMPLE RETURNS
#


class Returns():
  def dividends():
    # Returns todays date and the total dividends paid
    today = str(date.today())
    divi = round(rh.account.get_total_dividends(), 2)
    print(f'As of {today} you have made {divi} in dividends')
    return [[today, divi]]

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
    
  def cash():
    cash = float(rh.profiles.load_account_profile('cash'))
    return cash


#
#              DATA MANIPULATION
#


class RecordData():
  def buildCSV():
    # Exports position data to csv for importing into DivTracker
    tickers = []
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
      itter = {
        'Ticker': ticker,
        'Quantity': shares,
        'Cost Per Share': cost,
        'Date': today
      }
      resolved.append(itter)
    print('Generating CSV')
    with open('data/positions.csv', 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=field_names)
      writer.writeheader()
      writer.writerows(resolved)
    print('File exported as positions.csv')

  def buildIndex():
    # creates a table for storing ticker names
    curs.execute("create table if not exists tickers" + " (ticker text)")
    # reads the ticker names from positions and outputs them as a column in the "tickers" table in the "positions" database
    data = pd.read_csv('data/positions.csv', usecols=['Ticker'])
    data.to_sql('tickers', connection, if_exists='replace', index=True)
    # close the database
    connection.close()

  def divi():
    curs.execute("create table if not exists dividends" +"(date text, dividends int)")
    data = Returns.dividends()
    df = pd.DataFrame(data, columns = ['date', 'dividends'])
    df.to_sql('dividends',connection,      if_exists='replace',index=False)
    connection.close

