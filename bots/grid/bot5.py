import robin_stocks as r
import time

# Setup Robinhood API credentials
r.login(username="<your_username>", password="<your_password>")

# Set initial trade parameters
pair = "BTC-USD"
price_floor = 50000
price_cap = 55000
grid_size = 10
qty = 0.0001

# Create grid
buy_prices = []
sell_prices = []
for i in range(price_floor, price_cap + grid_size, grid_size):
    buy_prices.append(i)
    sell_prices.append(i + (grid_size / 2))

# Trading loop
while True:
    # Get current price of pair
    curr_price = float(r.stocks.get_crypto(pair)['last_trade_price'])

    # Define buy/sell parameters
    for j in range(len(buy_prices)):
        if curr_price <= buy_prices[j]:
            buy_price = buy_prices[j]
            sell_price = sell_prices[j]
            break

    # Place buy order if necessary
    if r.crypto.get_buying_power() >= (qty * buy_price):
        r.orders.order_sell_crypto_by_price(pair, qty, buy_price)
        print(f"Bought {qty} {pair} at {buy_price}.")

    # Place sell order if necessary
    if r.crypto.get_quantity(pair) >= qty and curr_price >= sell_price:
        r.orders.order_sell_crypto_by_price(pair, qty, sell_price)
        print(f"Sold {qty} {pair} at {sell_price}.")

    # Print balances and profit/loss
    account_balance = float(r.crypto.get_account()['equity'])
    initial_balance = (buy_price - (grid_size / 2)) * qty
    profit_loss = account_balance - initial_balance
    print(f"Account balance: {account_balance}, Initial balance: {initial_balance}, Profit/loss: {profit_loss}")

    # Wait for specified period of time before continuing loop
    time.sleep(60)
