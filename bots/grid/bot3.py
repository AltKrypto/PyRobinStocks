import robin_stocks as r
import time

# Log in to robinhood account
r.login(username='<username>', password='<password>')

# Set up trading variables
buy_price = 56000  # lower limit price
sell_price = 58000  # upper limit price
increment = 100  # price difference between limit orders
quantity = 0.001  # amount of BTC to buy or sell
grid = []

# Calculate the grid based on the buy and sell prices and the increment
for i in range(int((sell_price - buy_price) / increment)):
    price = buy_price + (i * increment)
    grid.append(price)

# Place initial limit buy order
r.orders.order_sell_crypto_by_price('BTC', quantity, buy_price)

# Start grid trading
while True:
    try:
        # Get current BTCUSD price
        price = r.crypto.get_crypto_currency_pair('BTCUSD')['last_trade_price']

        # Compare price to grid and place limit orders
        for g in grid:
            if g > price:
                r.orders.order_sell_crypto_by_price('BTC', quantity, g)
            elif g < price:
                r.orders.order_buy_crypto_by_price('BTC', quantity, g)

        # Check for filled limit orders
        orders = r.orders.get_all_crypto_orders()
        for o in orders:
            if o['side'] == 'sell' and o['state'] == 'filled':
                sell_price = o['price']
                profit = (sell_price - buy_price) * quantity
                print(f"Sell Order Filled: Sell at {sell_price}, Profit: {profit:.4f}")

                # Reset the buy and sell prices based on the filled order
                buy_price = sell_price - increment
                sell_price = buy_price + (increment * 2)

                # Calculate the new grid
                grid = []
                for i in range(int((sell_price - buy_price) / increment)):
                    price = buy_price + (i * increment)
                    grid.append(price)

                # Place new limit buy order
                r.orders.order_sell_crypto_by_price('BTC', quantity, buy_price)

            elif o['side'] == 'buy' and o['state'] == 'filled':
                buy_price = o['price']
                print(f"Buy Order Filled: Buy at {buy_price}")

                # Place new limit sell order
                sell_price = buy_price + increment
                r.orders.order_buy_crypto_by_price('BTC', quantity, sell_price)

        # Real-time monitoring
        print(f"Current BTCUSD Price: {price:.2f}")
        print(f"Buy Price: {buy_price}, Sell Price: {sell_price}")
        time.sleep(10)

    except Exception as e:
        print(e)
        continue
