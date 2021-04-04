import time
import config
import helpers.time_helper as time_helper
import threading

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

    def refresh(self):
        self.price.append(self.query_source.get_price(self.ticker))
        for indicator in self.indicators:
            if self.indicators[indicator] == []:  # not initialized. fetch all data since market open
                start_timestamp = time_helper.today_opening_timestamp(self.config['marketOpen'])
            else:  # updating the data. let's just query the missing data.
                start_timestamp = self.indicators[indicator][len(self.indicators[indicator]) - 1][
                    'timestamp']  # timestamp of last entry

            end_timestamp = int(time.time())
            data = self.query_source.get_indicator(self.ticker, indicator, start_timestamp, end_timestamp,
                                                   params=self.config['indicators'][indicator]['params'])
            if data is not None:
                for entry in data:
                    self.indicators[indicator].append(entry)


class Stocks:
    tickers = {}
    config=None
    max_concurrent_threads=0

    def __init__(self, stock_list, query_source):
        self.config=config.config
        for item in stock_list:
            self.tickers[item.strip()] = Stock(item, query_source)
        if len(self.tickers)>0:
            first_key=list(self.tickers.keys())[0]
            first_stock=self.tickers[first_key]
            self.max_concurrent_threads=first_stock.query_source.token_length * first_stock.query_source.max_poll_rate


    def refresh_thread(self,stock):
        stock.refresh()

    def refresh(self):
        # start up the max amount of concurrent threads. whenever a thread is finished, start another one

        current_threads=[]

        for stock in self.tickers:
            for thread in current_threads:  # remove finished threads
                if not thread.is_alive():
                    current_threads.remove(thread)

            if(len(current_threads)>=self.max_concurrent_threads):  # if threads maxed out, wait
                oldest_thread=current_threads[0]
                oldest_thread.join()

            this_thread=threading.Thread(target=self.refresh_thread,args=(self.tickers[stock],))
            current_threads.append(this_thread)
            this_thread.start()

        if(len(current_threads)>0): # wait for all threads to finish before returning
            for thread in current_threads:
                thread.join()
