import robin_stocks as r
import time

# Login to Robinhood account
r.login(username="YOUR_USERNAME", password="YOUR_PASSWORD")

# Define grid parameters
grid_spacing = 50  # how far apart each grid order should be (in dollars)
grid_levels = 10  # how many grid levels to place on each side of the current price
min_buy_price = 30000  # the minimum price at which to buy BTC
max_sell_price = 60000  # the maximum price at which to sell BTC
buy_quantity = 0.001  # how much BTC to buy for each grid order
sell_quantity = 0.001  # how much BTC to sell for each grid order

# Place initial buy order
current_price = float(r.crypto.get_crypto('BTC')['mark_price'])
buy_price = current_price - (grid_spacing * grid_levels)
if buy_price < min_buy_price:
    buy_price = min_buy_price
buy_order = r.orders.order_sell_crypto_limit('BTC', buy_quantity, buy_price)

# Place initial sell order
sell_price = current_price + (grid_spacing * grid_levels)
if sell_price > max_sell_price:
    sell_price = max_sell_price
sell_order = r.orders.order_sell_crypto_limit('BTC', sell_quantity, sell_price)

# Main loop
while True:
    # Check if any orders have been filled
    orders = r.orders.get_all_crypto_orders()
    for order in orders:
        if order['state'] == 'filled':
            # Determine profit/loss from filled order
            if order['side'] == 'sell':
                entry_price = float(order['executions'][0]['price'])
                exit_price = float(order['price'])
                profit_loss = (sell_quantity * exit_price) - (buy_quantity * entry_price)
            else:
                entry_price = float(order['price'])
                exit_price = float(order['executions'][0]['price'])
                profit_loss = (sell_quantity * exit_price) - (buy_quantity * entry_price)
            print('Filled order:', order['side'], order['executions'][0]['quantity'], 'BTC at', entry_price,
                  'for a profit/loss of', profit_loss, 'USD')

            # Place new order on opposite side of grid
            current_price = float(r.crypto.get_crypto('BTC')['mark_price'])
            if order['side'] == 'sell':
                buy_price = current_price - (grid_spacing * grid_levels)
                if buy_price < min_buy_price:
                    buy_price = min_buy_price
                buy_order = r.orders.order_sell_crypto_limit('BTC', buy_quantity, buy_price)
            else:
                sell_price = current_price + (grid_spacing * grid_levels)
                if sell_price > max_sell_price:
                    sell_price = max_sell_price
                sell_order = r.orders.order_sell_crypto_limit('BTC', sell_quantity, sell_price)

    # Print current grid levels
    print('Current grid levels:')
    for i in range(grid_levels):
        buy_price = current_price - (grid_spacing * (i + 1))
        sell_price = current_price + (grid_spacing * (i + 1))
        print('Buy at', buy_price, 'Sell at', sell_price)
    print()

    # Wait 10 seconds before checking again
    time.sleep(10)
