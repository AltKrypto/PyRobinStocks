import robin_stocks.robinhood as rh
from usermethods import *
import os
os.system('dbmodules/dbmethods.py')

login()

divTrackCsv()

tickerTable()

cleanUp()