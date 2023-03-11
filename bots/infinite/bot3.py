import robin_stocks as r
import time

# Set up login credentials
r.login(username='your_username', password='your_password')

# Constants for trading settings
GRID_SPACING = 100   # How far apart (in USD) each order in the grid should be
GRID_SIZE = 10       # How many orders should be placed on each side of the current price

# Keep track of profit/loss and buying power
pl = 0
buying_power = float(r.profiles.load_account_profile()['buying_power'])

# Start dynamic bidding loop
while True:
    # Get current BTCUSD price
    price = float(r.stocks.get_crypto('BTC')['last_trade_price'])

    # Place sell orders if existing orders are profitable
    open_orders = r.orders.get_crypto_orders()
    for order in open_orders:
        if order['side'] == 'sell' and order['state'] == 'filled':
            pl += float(order['executed_notional']) - float(order['price']) * float(order['executed_quantity'])
            buying_power += float(order['executed_notional'])
            print(f"Sold {order['executed_quantity']} BTC at {order['price']}.")
    time.sleep(1)

    # Place buy orders at predetermined intervals
    for i in range(-GRID_SIZE, GRID_SIZE+1):
        if (i * GRID_SPACING + price) > 0 and buying_power > price * GRID_SPACING:
            order = r.orders.order_sell_crypto_limit('BTC', GRID_SPACING + price + i * GRID_SPACING, GRID_SPACING / price)
            print(f"Placed sell order for {GRID_SPACING/price} BTC at {GRID_SPACING+price+i*GRID_SPACING}.")
            buying_power -= price * GRID_SPACING
    time.sleep(1)

    # Place sell orders at predetermined intervals
    for i in range(-GRID_SIZE, GRID_SIZE+1):
        if (price - i * GRID_SPACING) > 0:
            order = r.orders.order_buy_crypto_limit('BTC', price - i * GRID_SPACING, GRID_SPACING / price)
            print(f"Placed buy order for {GRID_SPACING/price} BTC at {price-i*GRID_SPACING}.")
    time.sleep(1)

    # Print current profit/loss and available buying power
    print(f"Profit/Loss: {pl:,.2f} USD")
    print(f"Buying power: {buying_power:,.2f} USD")
