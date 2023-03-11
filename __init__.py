import robin_stocks.robinhood as rh
from methods import * 

Session.login()

cash = Returns.cash()
print(cash)
Returns.dividends()

Session.logout()