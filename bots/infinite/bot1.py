import robin_stocks as r
import time

# Define settings for the bot
starting_price = float(r.crypto.get_crypto_currency_pairs('BTC', 'USD')['min_order_size'])
grid_scale = 0.01    # The distance between each grid line
total_balance = float(r.crypto.get_crypto_currency_pairs('BTC', 'USD')['min_order_size'])    # Initial balance

# Infinitely loop while checking the current BTC price
while True:
    # Get the current price of BTC
    current_price = float(r.crypto.get_crypto_quote('BTC')['last_trade_price'])
    
    # Calculate the current grid lines
    upper_line = starting_price * (1 + grid_scale)
    lower_line = starting_price * (1 - grid_scale)
    
    # Check if any grid line has been hit
    if current_price >= upper_line:
        # Sell BTC to create a new upper grid line
        r.orders.order_sell_crypto_by_price('BTC', total_balance)
        total_balance += total_balance * grid_scale
        starting_price = upper_line
        
    elif current_price <= lower_line:
        # Buy BTC to create a new lower grid line
        r.orders.order_buy_crypto_by_price('BTC', total_balance)
        total_balance += total_balance * grid_scale
        starting_price = lower_line
        
    # Check if there are any open orders
    open_orders = r.orders.get_all_open_crypto_orders()
    for order in open_orders:
        # Calculate the profit/loss for each open order
        order_id = order['id']
        order_type = order['side']
        order_price = float(order['price'])
        order_size = float(order['quantity'])
        current_value = order_size * current_price
        
        if order_type == 'sell':
            profit_loss = (current_value - (order_size * order_price)) / (order_size * order_price)
        else:
            profit_loss = ((order_size * order_price) - current_value) / (order_size * order_price)
        
        # Print the order's current status
        print(f"{order_id} | {order_type} | {order_price:.2f} | {order_size:.8f} | {current_value:.2f} | {profit_loss:.2%}")
    
    # Wait for a few seconds before checking again
    time.sleep(10)
