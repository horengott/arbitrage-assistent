import ccxt.async_support as ccxt
import asyncio  
import time


# checking liquidity:

async def calculate_vwap(order_book_side, target_amount_usdt):
        remaining_usdt = target_amount_usdt
        total_tokens = 0
    
        for i in range(len(order_book_side)):
            level_price = order_book_side[i][0]
            level_volume = order_book_side[i][1]
        
            level_total_cost = level_price * level_volume
        
            if remaining_usdt <= level_total_cost:
                bought_tokens = remaining_usdt / level_price
                total_tokens += bought_tokens
                remaining_usdt = 0
                break 
            else:
                total_tokens += level_volume
                remaining_usdt -= level_total_cost
            
        if remaining_usdt > 0:
            return None 

        return target_amount_usdt / total_tokens


async def get_liquid_exchanges(exchanges, token_symbol, user_balance_usdt):
        symbol = f"{token_symbol}/USDT"
    
        for exchange in exchanges:
            try:
                order_book = await exchange.fetch_order_book(symbol, limit=50)
            
                buy_price = await calculate_vwap(order_book['asks'], user_balance_usdt)
            
                sell_price =  await calculate_vwap(order_book['bids'], user_balance_usdt)
            
                if buy_price and sell_price:
                    yield {
                        'exchange': exchange.id,
                        'buy_price': buy_price,  
                        'sell_price': sell_price, 
                        'original_ask': order_book['asks'][0][0] 
                    }
                
            except Exception as e:
                continue



# getting the best ask/bid price:

async def find_best_route(token_symbol, user_balance_usdt):
    exchange_names = ['binance', 'bybit', 'okx', 'kucoin', 'gateio']
    
    exchanges = [getattr(ccxt, name)({'enableRateLimit': True}) for name in exchange_names]

    best_buy = {'exchange': None, 'price': float('inf')}
    best_sell = {'exchange': None, 'price': 0}

    print("searching the best price")

    async for market_data in get_liquid_exchanges(exchanges, token_symbol, user_balance_usdt):
        print(f"exchange {market_data['exchange']} is aproved by liquidity")
        print(f"real buy price: {market_data['buy_price']}")

        if market_data['buy_price'] < best_buy['price']:
            best_buy['exchange'] = market_data['exchange']
            best_buy['price'] = market_data['buy_price']

        if market_data['sell_price'] > best_sell['price']:
            best_sell['exchange'] = market_data['exchange']
            best_sell['price'] = market_data['sell_price']

    if best_buy['exchange'] and best_sell['exchange']:
        print(f"buying {best_buy['exchange']} by {best_buy['price']}")
        print(f"selling {best_sell['exchange']} by {best_sell['price']}")
        return best_buy, best_sell
    else:
        print("there are not liquidit routes")
        return None, None
        

