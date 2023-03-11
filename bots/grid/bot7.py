import robin_stocks as r
import time

# Login to Robinhood API
r.login() # Enter your username and password here

# Set up initial parameters
price_low = 5000
price_high = 9000
grid_size = 10
buy_levels = []
sell_levels = []

# Populate buy and sell levels for the price range and grid size
for i in range(grid_size+1):
    buy_price = price_low + ((price_high - price_low)/grid_size)*i
    sell_price = buy_price * 1.01 # 1% profit target
    buy_levels.append(buy_price)
    sell_levels.append(sell_price)

# Track current position and P/L
prev_position = r.crypto.get_crypto_currency_balance('BTC')
prev_balance = r.crypto.get_crypto_currency_balance('USD')

# Define function to monitor price and execute trades
def monitor_market():
    while True:
        current_price = r.crypto.get_crypto_currency('BTC', 'ask_price')
        print(f'Current price: {current_price}')

        # Check if price is in buy or sell range
        for i in range(len(buy_levels)):
            if current_price > buy_levels[i] and current_price < sell_levels[i]:
                # Buy order
                try:
                    r.order_buy_crypto_by_price('BTC', 1) # Buy 1 BTC
                    print('Buy order placed')
                except:
                    print('Buy order failed')

                # Sell order
                try:
                    r.order_sell_crypto_by_price('BTC', 1, sell_levels[i]) # Sell 1 BTC at sell price
                    print('Sell order placed')
                except:
                    print('Sell order failed')

        # Calculate P/L
        current_position = r.crypto.get_crypto_currency_balance('BTC')
        current_balance = r.crypto.get_crypto_currency_balance('USD')

        pl_position = current_position - prev_position
        pl_balance = current_balance - prev_balance

        print(f'Current position: {current_position}\n'
              f'P/L on position: {pl_position}\n'
              f'Current balance: {current_balance}\n'
              f'P/L on balance: {pl_balance}')

        # Update previous position and balance
        prev_position = current_position
        prev_balance = current_balance

        time.sleep(60) # Wait 1 minute before checking price again

monitor_market()
