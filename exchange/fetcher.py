import ccxt.async_support as ccxt
import asyncio  
import time

# get list of exchanges:

def get_exchanges():
    return ccxt.exchanges


# getting the best ask price:

async def best_ask(token):
    
        best_ask_price = {
            'price': 100000000,
            'amount': 0,
            'exchange': None
        }

        print("starting...")
        bolsas = 0

        for exchange in ['binance', 'bybit', 'okx', 'kucoin', 'gateio']:
            print(f"checking: {exchange}")
            ex = getattr(ccxt, exchange)
            current_exchange = ex({'timeout': 3000, 'enableRateLimit': True})
        
            try:

                await current_exchange.load_markets()

                if token in current_exchange.symbols:
                    orderbook = await current_exchange.fetch_order_book(token, limit=20)

                    print(f"se va a ver: {orderbook['asks'][0][0]} de {exchange}")

                    if orderbook['asks'][0][0] < best_ask_price['price']:
                        best_ask_price['price'] = orderbook['asks'][0][0]
                        best_ask_price['amount'] = orderbook['asks'][0][1]
                        best_ask_price['exchange'] = exchange
                        print(f" lo que entra en el if: {best_ask_price}")
                        bolsas += 1
                    else:
                        continue
                else:
                    continue



            except ccxt.BaseError as e:
                print(f"error de ccxt: {exchange}")
                continue

            except Exception as e:
                print(f"error desconocido: {exchange}")
                continue

            finally:
                await current_exchange.close()
        
        print(f"el mejor precio es en {best_ask_price['exchange']}")
        return f"el mejor precio es en {best_ask_price['exchange']}"
        

# getting the best ask price:

async def best_bid(token):
    
        best_bid_price = {
            'price': 0,
            'amount': 0,
            'exchange': None
        }

        print("starting...")
        bolsas = 0

        for exchange in ['binance', 'bybit', 'okx', 'kucoin', 'gateio']:
            print(f"checking: {exchange}")
            ex = getattr(ccxt, exchange)
            current_exchange = ex({'timeout': 3000, 'enableRateLimit': True})
        
            try:

                await current_exchange.load_markets()

                if token in current_exchange.symbols:
                    orderbook = await current_exchange.fetch_order_book(token, limit=20)

                    print(f"se va a ver: {orderbook['bids'][0][0]} de {exchange}")

                    if orderbook['bids'][0][0] > best_bid_price['price']:
                        best_bid_price['price'] = orderbook['bids'][0][0]
                        best_bid_price['amount'] = orderbook['bids'][0][1]
                        best_bid_price['exchange'] = exchange
                        print(f" lo que entra en el if: {best_bid_price}")
                        bolsas += 1
                    else:
                        continue
                else:
                    continue



            except ccxt.BaseError as e:
                print(f"error de ccxt: {exchange}")
                continue

            except Exception as e:
                print(f"error desconocido: {exchange}")
                continue

            finally:
                await current_exchange.close()
        
        print(f"el mejor precio es en {best_bid_price['exchange']}")
        return f"el mejor precio es en {best_bid_price['exchange']}"

asyncio.run(best_bid("ETH/USDT"))