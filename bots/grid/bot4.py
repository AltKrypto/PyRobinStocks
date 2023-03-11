import robin_stocks as r
import time

# Login to Robinhood
login = r.login('your_username', 'your_password')
symbols = ['BTCUSD']  # list of symbols to trade
increment = 20  # $ increment at each level
levels = 5  # number of levels in the grid
max_orders = 5  # maximum number of open orders

# initialize order books and trade stats
order_books = {symbol: [] for symbol in symbols}
stats = {symbol: {'p&l': 0, 'sell_count': 0, 'buy_count': 0} for symbol in symbols}

# calculate the grid prices
current_price = float(r.crypto.get_crypto_currency_pair('BTCUSD')['mark_price'])
grid_prices = [round(current_price + i*increment, 2) for i in range(-levels//2+1, levels//2+1)]

# enter the trading loop to monitor & trade
while True:
    for symbol in symbols:
        # check for open orders
        orders = r.orders.get_crypto_orders_by_symbol(symbol)
        open_orders = []
        for order in orders:
            if order['state'] == 'queued' or order['state'] == 'confirmed':
                open_orders.append(order)
        
        # cancel excess orders
        while len(open_orders) > max_orders:
            order_to_cancel = open_orders.pop(0)
            r.orders.cancel_crypto_order(order_to_cancel['id'])
        
        # update order book
        order_books[symbol] = open_orders
        
        # calculate the average buy & sell prices
        buy_prices = [order['price'] for order in order_books[symbol] if order['side'] == 'buy']
        sell_prices = [order['price'] for order in order_books[symbol] if order['side'] == 'sell']
        if not buy_prices:
            avg_buy_price = 0
        else:
            avg_buy_price = sum(buy_prices) / len(buy_prices)
        if not sell_prices:
            avg_sell_price = 0
        else:
            avg_sell_price = sum(sell_prices) / len(sell_prices)
        
        # place buy & sell orders at grid prices
        for i, price in enumerate(grid_prices):
            if price < avg_buy_price and len([order for order in order_books[symbol] if order['side'] == 'buy']) < max_orders:
                order = r.orders.order_sell_crypto_by_price(symbol, price, 0.001)
                order_books[symbol].append(order)
                stats[symbol]['buy_count'] += 1
            elif price > avg_sell_price and len([order for order in order_books[symbol] if order['side'] == 'sell']) < max_orders:
                order = r.orders.order_buy_crypto_by_price(symbol, price, 0.001)
                order_books[symbol].append(order)
                stats[symbol]['sell_count'] += 1
    
    # update trade stats
    for symbol in symbols:
        for order in order_books[symbol]:
            if order['side'] == 'buy':
                stats[symbol]['p&l'] -= order['price'] * order['quantity'] * 0.005
            elif order['side'] == 'sell':
                stats[symbol]['p&l'] += order['price'] * order['quantity'] * 0.995
    
    # print the order book and trade stats
    print(f'---- {time.ctime()} ----')
    for symbol in symbols:
        print(f'{symbol}:')
        for order in order_books[symbol]:
            print(f'\t{order["side"]} {order["price"]} {order["state"]}')
        print(f'\tbuys: {len([order for order in order_books[symbol] if order["side"] == "buy"])} sells: {len([order for order in order_books[symbol] if order["side"] == "sell"])}')
        print(f'\tp&l: {stats[symbol]["p&l"]:.2f} buys: {stats[symbol]["buy_count"]} sells: {stats[symbol]["sell_count"]}')
    
    # sleep for 10 seconds before running the loop again
    time.sleep(10)
