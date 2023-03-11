import robin_stocks as r
import time

# Fill in your Robinhood login credentials or load from a file.
username = "your_username"
password = "your_password"
r.login(username, password)

# Define the parameters for the grid trading
start_price = 50000  # Starting price of the asset
grid_size = 15.0     # Price difference between each grid
num_grids = 50       # Number of grids on each side of the starting price
investment = 100     # Amount of currency to invest

# Define some helper functions
def get_price():
    return float(r.crypto.get_crypto_currency_quote('BTC')['mark_price'])

def get_portfolio_value():
    return float(r.crypto.get_crypto_currency_quote('USD')['mark_price'])

# Create the grid
prices = [start_price + i*grid_size for i in range(-num_grids, num_grids+1)]

# Loop through the grid and place orders
for price in prices:
    target_price = round(price, 2)  # Round to 2 decimal places
    order_type = 'buy' if price < start_price else 'sell'
    order_quantity = investment / target_price
    order_status = r.orders.order_sell_limit('BTCUSD', order_quantity, target_price) if order_type == 'sell' else r.orders.order_buy_limit('BTCUSD', order_quantity, target_price)
    print(f"{'Sell' if order_type == 'sell' else 'Buy'} order placed at {target_price} with quantity {order_quantity} with status {order_status['status']}")
    time.sleep(5)

# Monitor the prices and calculate profit/loss
while True:
    current_price = get_price()
    portfolio_value = get_portfolio_value()
    print(f"Current price: {current_price}, Portfolio value: {portfolio_value}")
    for i, price in enumerate(prices):
        if current_price >= price and ('sell' in order_status['side'] if price < start_price else 'buy' in order_status['side']):
            target_price = round(prices[i+1] if price < start_price else prices[i-1], 2)
            order_type = 'buy' if price < start_price else 'sell'
            order_quantity = investment / target_price
            order_status = r.orders.order_sell_limit('BTCUSD', order_quantity, target_price) if order_type == 'sell' else r.orders.order_buy_limit('BTCUSD', order_quantity, target_price)
            print(f"{'Sell' if order_type == 'sell' else 'Buy'} order placed at {target_price} with quantity {order_quantity} with status {order_status['status']}")
    profit_loss = portfolio_value - investment
    print(f"Profit/Loss: {profit_loss}")
    time.sleep(5)
