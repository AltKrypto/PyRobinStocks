from os import environ
from dotenvy import load_env, read_file
import pyotp
import robin_stocks.robinhood as rh
from datetime import date

def login():
    load_env(read_file('.env'))
    user = environ.get('username')
    passw = environ.get('password')
    auth = environ.get('auth')
    totp = pyotp.TOTP(auth).now()
    login = rh.login(user, passw, mfa_code = totp)

def dividends():
    today = str(date.today())
    divi = round(rh.account.get_total_dividends(), 2)
    return [today, divi]

def account():
    pass