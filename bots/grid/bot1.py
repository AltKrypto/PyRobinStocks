import robin_stocks as r
import time

# Set up login credentials
r.login(username='your_username', password='your_password')

# Set up grid trading parameters
start_price = 35000
price_range = 5000
num_orders = 5

# Calculate grid levels
levels = []
for i in range(num_orders):
    level_price = start_price + (i * price_range)
    levels.append(level_price)

# Place initial buy order at the lowest level
buy_order = r.orders.order_sell_crypto_by_price('BTC', 1, levels[0])

# Place sell orders at all other levels
sell_orders = []
for i in range(1, num_orders):
    sell_order = r.orders.order_sell_crypto_by_price('BTC', 1, levels[i])
    sell_orders.append(sell_order)

# Start grid trading loop
while True:
    # Check for filled orders
    open_orders = r.orders.get_all_crypto_orders()
    for order in open_orders:
        if order['side'] == 'buy' and order['state'] == 'filled':
            # If a buy order is filled, place a sell order at the next level
            filled_level = levels.index(float(order['price']))
            if filled_level < num_orders - 1:
                sell_order = r.orders.order_sell_crypto_by_price('BTC', 1, levels[filled_level + 1])
                sell_orders.append(sell_order)
        elif order['side'] == 'sell' and order['state'] == 'filled':
            # If a sell order is filled, place a buy order at the lowest level
            buy_order = r.orders.order_buy_crypto_by_price('BTC', 1, levels[0])

    # Wait for one minute before checking again
    time.sleep(60)
