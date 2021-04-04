import time
import config
import helpers.time_helper as time_helper
import threading

''' Class for an individual stock '''
class Stock:
    config = config.config
    ticker = ""
    query_source = None
    price = []
    indicators = {}


    def __init__(self, ticker, query_source):
        self.ticker = ticker
        self.query_source = query_source
        for indicator in self.config['indicators']:
            self.indicators[indicator] = []

    ''' Fetch the latest data from the API'''
    def refresh(self):
        price_result=self.query_source.get_price(self.ticker)
        if price_result is not None:
            self.price.append()

        for indicator in self.indicators:
            if self.indicators[indicator] == []:  # Data not initialized. fetch all data since market open
                start_timestamp = time_helper.today_opening_timestamp(self.config['marketOpen'])
            else:  # Updating the data. let's just query the missing data.
                start_timestamp = self.indicators[indicator][len(self.indicators[indicator]) - 1][
                    'timestamp']  # timestamp of last entry

            end_timestamp = int(time.time())
            data = self.query_source.get_indicator(self.ticker, indicator, start_timestamp, end_timestamp,
                                                   params=self.config['indicators'][indicator]['params'])
            if data is not None:
                for entry in data:
                    self.indicators[indicator].append(entry)


''' Class that holds multiple Stock objects '''
class Stocks:
    tickers = {}
    config=None
    max_concurrent_threads=0

    def __init__(self, stock_list, query_source):
        self.config=config.config

        for item in stock_list:
            self.tickers[item.strip()] = Stock(item, query_source)
        if len(self.tickers)>0:
            first_key=list(self.tickers.keys())[0]  # Just get the config from the first ticker. It should be the same for all tickers in the list..
            first_stock=self.tickers[first_key]

            # Max number of parallel threads is equal to the number of tokens we have x number of requests per token allowed per second
            self.max_concurrent_threads=first_stock.query_source.token_length * first_stock.query_source.max_poll_rate


    def refresh_thread(self,stock): # Thread that calls the refresh method for a given stock
        stock.refresh()

    def refresh(self): # Method used to refresh all stocks.

        # Start up the max amount of concurrent threads. whenever a thread is finished, start another one
        current_threads=[]
        for stock in self.tickers:
            for thread in current_threads:  # Remove finished threads
                if not thread.is_alive():
                    current_threads.remove(thread)

            if(len(current_threads)>=self.max_concurrent_threads):  # If number of threads are maxed out, wait before starting new threads.
                oldest_thread=current_threads[0]
                oldest_thread.join()    # join() blocks code execution.

            # If we get here, at least one thread can be started.
            this_thread=threading.Thread(target=self.refresh_thread,args=(self.tickers[stock],))
            current_threads.append(this_thread)
            this_thread.start()

        # If we get here, threads have been started for all the ticker.
        if(len(current_threads)>0): # Wait for all threads to finish before returning
            for thread in current_threads:
                thread.join()
