import ccxt.async_support as ccxt
import asyncio
import json

def calculate_vwap(order_book_side, target_amount_usdt):
    remaining_usdt = target_amount_usdt
    total_tokens = 0

    for price, volume in order_book_side:
        level_total_cost = price * volume

        if remaining_usdt <= level_total_cost:
            total_tokens += remaining_usdt / price
            remaining_usdt = 0
            break
        else:
            total_tokens += volume
            remaining_usdt -= level_total_cost

    return target_amount_usdt / total_tokens if remaining_usdt == 0 else None

async def fetch_market_data(exchange, symbol, user_balance_usdt):
    try:
        order_book = await exchange.fetch_order_book(symbol, limit=50)
        buy_price = calculate_vwap(order_book['asks'], user_balance_usdt)
        sell_price = calculate_vwap(order_book['bids'], user_balance_usdt)

        if buy_price and sell_price:
            return {
                'exchange': exchange.id,
                'buy_price': buy_price,
                'sell_price': sell_price
            }
    except:
        return None
    return None

async def find_best_route(token_symbol, user_balance_usdt):
    symbol = f"{token_symbol}/USDT"
    exchange_names = ['binance', 'bybit', 'okx', 'kucoin', 'gateio']

    exchanges = [getattr(ccxt, name)({
        'enableRateLimit': True, 
        'timeout': 5000
    }) for name in exchange_names]

    try:
        print(f"🔎 Fetching prices from {len(exchange_names)} exchanges for {symbol}...")
        tasks = [fetch_market_data(ex, symbol, user_balance_usdt) for ex in exchanges]
        results = await asyncio.gather(*tasks)

        valid_markets = [r for r in results if r is not None]
        print(f"✅ Data retrieved from: {[m['exchange'] for m in valid_markets]}")

        if len(valid_markets) < 2:
            return None, None

        best_spread = -float('inf')
        best_buy_found = None
        best_sell_found = None

        for buy_mkt in valid_markets:
            for sell_mkt in valid_markets:
                if buy_mkt['exchange'] == sell_mkt['exchange']:
                    continue

                current_spread = (sell_mkt['sell_price'] - buy_mkt['buy_price']) / buy_mkt['buy_price']

                if current_spread > best_spread:
                    best_spread = current_spread
                    best_buy_found = buy_mkt
                    best_sell_found = sell_mkt

        if best_buy_found:
            print(f"📈 Best mathematical route: {best_buy_found['exchange']} -> {best_sell_found['exchange']} (Gross Spread: {round(best_spread*100, 3)}%)")

        return best_buy_found, best_sell_found

    finally:
        await asyncio.gather(*[exchange.close() for exchange in exchanges])

try:
    with open('config_fees.json', 'r', encoding='utf-8') as f:
        FEES_CONFIG = json.load(f)
        print("✅ Fee configuration loaded successfully.")
except FileNotFoundError:
    FEES_CONFIG = {}
    print("⚠️ config_fees.json not found, using default values.")

async def calculate_arbitrage_result(amount_usdt, buy_price, sell_price, symbol):
    base_coin = symbol.split('/')[0]
    
    trade_fee_pct = FEES_CONFIG.get('trading_fees', {}).get('default_taker', 0.001)
    
    coin_fees = FEES_CONFIG.get('withdrawal_fees', {}).get(base_coin)
    
    if coin_fees:
        withdraw_fee_amount = coin_fees['default_fee']
        print(f"ℹ️ Withdrawal fee detected for {base_coin}: {withdraw_fee_amount} (Network: {coin_fees.get('network', 'Unknown')})") 
    else:
        withdraw_fee_amount = 1.0 / buy_price
        print(f"⚠️ Using generic withdrawal fee ($1.00)")

    amount_after_buy_fee = amount_usdt * (1 - trade_fee_pct)
    coins_bought = amount_after_buy_fee / buy_price
    
    coins_arrived = coins_bought - withdraw_fee_amount
    
    if coins_arrived <= 0:
        return {
            'success': False,
            'profit_usd': -amount_usdt,
            'profit_pct': -100.0,
            'withdraw_fee_paid': withdraw_fee_amount
        }
        
    usdt_received = (coins_arrived * sell_price) * (1 - trade_fee_pct)
    
    net_profit_usd = usdt_received - amount_usdt
    net_profit_pct = (net_profit_usd / amount_usdt) * 100
    
    return {
        'success': True,
        'profit_usd': round(net_profit_usd, 2),
        'profit_pct': round(net_profit_pct, 2),
        'withdraw_fee_paid': withdraw_fee_amount,
        'coin': base_coin
    }

async def get_arbitrage_analysis(token_symbol, amount_usdt):
    
    best_buy, best_sell = await find_best_route(token_symbol, amount_usdt)
    
    if not best_buy or not best_sell:
        print("❌ No sufficient liquidity found.")
        return {
            "found": False,
            "message": "No liquidity found"
        }
    
    symbol = f"{token_symbol}/USDT"
    
    result = await calculate_arbitrage_result(
        amount_usdt, 
        best_buy['buy_price'], 
        best_sell['sell_price'], 
        symbol
    )
    
    print(f"\n📊 --- FINAL SUMMARY FOR {symbol} ---")
    print(f"Buy: {best_buy['exchange']} @ {best_buy['buy_price']}")
    print(f"Sell: {best_sell['exchange']} @ {best_sell['sell_price']}")
    print(f"Profit: ${result['profit_usd']} ({result['profit_pct']}%)")
    print(f"---------------------------------------\n")

    if result['profit_usd'] > 0:
        return {
            "found": True,
            "buy_exchange": best_buy['exchange'],
            "buy_price": best_buy['buy_price'],
            "sell_exchange": best_sell['exchange'],
            "sell_price": best_sell['sell_price'],
            "analysis": result 
        }
    else:
        return {
            "found": False,
            "message": "No profitable route found (Negative Spread)"
        }