import time,threading
import components.stock as stock
import config

config=config.config

if config['main']['simulate']:
    from query_sources.simulator import Api as Api
else:
    from query_sources.query_source import Api as Api


query_source = Api()

with open('stocks.txt') as f:
    list_stocks=f.readlines()

stocks=stock.Stocks(list_stocks, query_source)

def poll_data():
    sleep_time=config['main']['poll_rate']
    while True:
        stocks.refresh()
        print(f"Polled new stock data at {time.time()}")
        time.sleep(sleep_time)

def analyze_data():
    sleep_time=config['main']['analyze_rate']
    while True:
        for stock_ticker in stocks.tickers:
            if(stocks.tickers[stock_ticker].has_data):
                pass    # send the data to analyze here...

        print(f"Analyzed stock data at {time.time()}")
        time.sleep(sleep_time)



refresh_thread=threading.Thread(target=poll_data)
refresh_thread.start()
analyze_thread=threading.Thread(target=analyze_data)
analyze_thread.start()

time.sleep(10)
print('done')
