import robin_stocks as r
import time

# Replace placeholders with actual Robinhood API credentials
login = r.login(username='USERNAME', password='PASSWORD')

INFINITY = float('inf')
PRICE_INCREMENT = 10     # This is the price increment for the grid
MAX_PRICE = 60000        # Maximum price that we expect BTC to reach
MIN_PRICE = 30000        # Minimum price that we expect BTC to reach
GRID_UPPER_LIMIT = MAX_PRICE + (MAX_PRICE - MIN_PRICE)     # Upper limit of the grid
GRID_LOWER_LIMIT = MIN_PRICE - (MAX_PRICE - MIN_PRICE)     # Lower limit of the grid

# To keep track of the grids we build
# This is a list of tuples of (price, shares)
# The shares will be dynamic and depend on how much total capital we have
grids = [(MIN_PRICE, 0), (MIN_PRICE + PRICE_INCREMENT, 0)]

# We will start with $10000 in our account
account_balance = r.crypto.get_crypto_currency_balance('BTC', 'currency')
total_balance_usd = float(r.crypto.get_crypto_currency_balance('USD', 'account')[0]['amount'])
total_balance_btc = float(account_balance[0]['amount'])

# Calculate the total capital that we have in USD
total_capital = total_balance_usd + total_balance_btc * r.crypto.get_crypto('BTC', info='market_price')

while True:
    # Get the current market price of BTC
    market_price = float(r.crypto.get_crypto('BTC', info='market_price'))

    # Calculate how many grids we need to build
    num_grids_needed = int((market_price - MIN_PRICE) // PRICE_INCREMENT) + 1

    # If we need to build more grids, build them
    while len(grids) < num_grids_needed:
        new_grid_price = grids[-1][0] + PRICE_INCREMENT
        grids.append((new_grid_price, 0))

    # If the market price is out of our grid, we need to buy or sell to adjust
    if market_price < grids[0][0]:
        # Buy one share at the top and move it to the bottom
        top_grid_price, top_grid_shares = grids[-1]
        r.crypto.order_buy_crypto_limit('BTC', top_grid_shares + 1, top_grid_price)
        r.crypto.order_sell_crypto_limit('BTC', top_grid_shares + 1, grids[0][0] - PRICE_INCREMENT)
        top_grid_shares += 1
        grids[-1] = (top_grid_price, top_grid_shares)

    elif market_price > grids[-1][0]:
        # Sell one share at the bottom and move it to the top
        bottom_grid_price, bottom_grid_shares = grids[0]
        r.crypto.order_sell_crypto_limit('BTC', bottom_grid_shares + 1, bottom_grid_price)
        r.crypto.order_buy_crypto_limit('BTC', bottom_grid_shares + 1, grids[-1][0] + PRICE_INCREMENT)
        bottom_grid_shares += 1
        grids[0] = (bottom_grid_price, bottom_grid_shares)

    # Calculate the total value of our position
    position_value_btc = 0
    for grid_price, grid_shares in grids:
        grid_value_btc = grid_shares * (GRID_UPPER_LIMIT - grid_price)
        position_value_btc += grid_value_btc

    position_value_usd = position_value_btc * r.crypto.get_crypto('BTC', info='market_price')

    # Calculate the profit/loss and print it out
    pnl = position_value_usd - total_capital
    print('Position Value: {0:.2f} USD, PnL: {1:.2f} USD'.format(position_value_usd, pnl))

    # Wait for a few seconds before repeating the loop
    time.sleep(10)
