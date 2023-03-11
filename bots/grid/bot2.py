import robin_stocks as r
import time

# Set Robinhood credentials
username = "your_username"
password = "your_password"
r.login(username, password)

# Set grid parameters
grid_size = 10
increment = 100
start_price = float(r.crypto.get_crypto_currency_pairs("BTC-USD")[0]['min_order_size']) + increment
end_price = start_price + (grid_size - 1) * increment

# Calculate trade amounts
balance = float(r.crypto.get_crypto_currency_account('BTC')['amount'])
amount_per_trade = balance / grid_size

# Place initial buy order
buy_order = r.crypto.order_sell_crypto_by_price('BTC-USD', amount_per_trade, end_price)

# Monitor price and place subsequent orders
while True:
    price = float(r.crypto.get_crypto_currency_pairs("BTC-USD")[0]['mark_price'])
    if price >= start_price:
        current_order_side = 'sell'
        current_price = start_price
        target_price = current_price + increment
    elif price <= end_price:
        current_order_side = 'buy'
        current_price = end_price
        target_price = current_price - increment
    else:
        time.sleep(60) # Wait for a minute before checking price again
        continue

    # Place trade order
    if current_order_side == 'sell':
        # Calculate sell price and profit/loss
        sell_price = current_price - (current_price - price) / grid_size
        pnl = (price - sell_price) * amount_per_trade
        order = r.crypto.order_sell_crypto_by_price('BTC-USD', amount_per_trade, sell_price)
    else:
        # Calculate buy price and profit/loss
        buy_price = current_price + (price - current_price) / grid_size
        pnl = (buy_price - price) * amount_per_trade
        order = r.crypto.order_buy_crypto_by_price('BTC-USD', amount_per_trade, buy_price)

    # Print order information
    print(f"{current_order_side} order placed: price={current_price}, amount={amount_per_trade}, target_price={target_price}, pnl={pnl}")

    # Set new current and target prices
    if current_order_side == 'sell':
        start_price = target_price
    else:
        end_price = target_price

    time.sleep(60) # Wait for a minute before placing the next order

# Logout from Robinhood
r.logout()
