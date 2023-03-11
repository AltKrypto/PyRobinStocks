import robin_stocks as r
import time

# Replace with your Robinhood login credentials
r.login("your_username", "your_password")

# Set up the parameters for the grid
initial_price = float(r.crypto.get_crypto_currency_pair("BTCUSD")['mark_price'])
lower_bound = initial_price * 0.9
upper_bound = initial_price * 1.1
grid_size = 10

# Initialize variables for tracking positions and profits
positions = []
profits = []

while True:
    # Get the current BTCUSD price
    price = float(r.crypto.get_crypto_currency_pair("BTCUSD")['mark_price'])

    # Place orders for the grid
    for i in range(grid_size):
        if i == 0:
            buy_price = lower_bound
        else:
            buy_price = (upper_bound - lower_bound) / (grid_size - 1) * i + lower_bound

        if buy_price < price and buy_price not in positions:
            # Buy at the grid price
            r.order_buy_crypto_limit("BTC", grid_size * 10, buy_price)
            positions.append(buy_price)

        if i == grid_size - 1:
            sell_price = upper_bound
        else:
            sell_price = (upper_bound - lower_bound) / (grid_size - 1) * (i+1) + lower_bound

        if sell_price > price and sell_price in positions:
            # Sell at the grid price
            r.order_sell_crypto_limit("BTC", grid_size * 10, sell_price)
            positions.remove(sell_price)

    # Monitor positions for profits and losses
    for pos in positions:
        order = r.orders.get_crypto_orders()[0]
        if order['price'] == pos:
            # Update the profit/loss for each position
            profit = (price - pos) / pos * 100
            profits.append(profit)
            positions[positions.index(pos)] = (pos, profit)

    # Remove any closed positions
    positions = [p for p in positions if isinstance(p, tuple)]

    # Print the current status of the bot
    print(f"BTCUSD: {price:.2f}")
    print(f"Positions: {positions}")
    print(f"Profits: {profits}")

    # Wait for a few seconds before checking again
    time.sleep(10)
