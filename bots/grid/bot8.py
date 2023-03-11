import robin_stocks as r
import time

# Set up authentication and login session
r.login(username="your_username", password="your_password")

# Define variables
increment = 10    # Set the price increment for grid lines
spread = 5        # Set the number of grid lines above and below the center price to place orders
quantity = 0.001  # Set the quantity of BTC to trade per order
profit = 0        # Set the profit goal in USD

# Get the current BTCUSD price
price = float(r.crypto.get_crypto('BTC')['last_trade_price'])

# Calculate the center price and grid lines
center = round(price, -1)
grid_lines = [center - spread * increment, center + spread * increment]

# Define a function to buy BTC
def buy(price):
    buy_price = round(price - increment/2, 2)
    r.orders.order_sell_crypto_by_price('BTC', quantity, buy_price, timeInForce='gtc')
    print("Buy order placed at", buy_price)

# Define a function to sell BTC
def sell(price):
    sell_price = round(price + increment/2, 2)
    r.orders.order_sell_crypto_by_price('BTC', quantity, sell_price, timeInForce='gtc')
    print("Sell order placed at", sell_price)

# Place initial buy and sell orders at the grid lines
buy(grid_lines[0])
sell(grid_lines[1])

# Set up a loop to monitor the market and adjust orders
while True:
    # Get the current BTCUSD price
    price = float(r.crypto.get_crypto('BTC')['last_trade_price'])
    print("Current price:", price)

    # Check if any orders have filled
    open_orders = r.orders.get_all_crypto_orders()
    for order in open_orders:
        if order['state'] == 'filled':
            if order['side'] == 'buy':
                sell(order['price'])
            elif order['side'] == 'sell':
                buy(order['price'])

    # Check if the profit goal has been reached
    account_value = float(r.crypto.get_crypto_currency('BTC')['equity'])
    current_profit = account_value - (quantity * (grid_lines[1] + grid_lines[0]) / 2)
    print("Current profit:", current_profit)
    if current_profit >= profit:
        break

    # Adjust orders to stay at the grid lines
    if price < grid_lines[0]:
        r.orders.cancel_all_crypto_orders()
        buy(grid_lines[0])
        sell(grid_lines[1])
    elif price > grid_lines[1]:
        r.orders.cancel_all_crypto_orders()
        buy(grid_lines[0])
        sell(grid_lines[1])

    # Wait a few seconds before checking again
    time.sleep(5)

# Log out of the session
r.logout()
