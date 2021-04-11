import time,random
import config

''' Provide simulated stock data for testing'''
class Api():
    config=None
    tokens=None
    token_length=0
    token = ''
    index=0
    max_poll_rate=0

    def __init__(self):
        self.config=config.config
        self.tokens=['abc','def']
        self.token_length=len(self.tokens)
        self.max_poll_rate=100
        self.tickers={}

    def get_starting_price(self):
        return random.randint(10,300)

    def get_next_value(self,prev_value):
        temp=random.randint(0,1)
        if temp==0:
            sign=-1
        else:
            sign=1

        # allow a +- difference of % of the previous price
        percent_difference=0.3
        lower_threshold=int(prev_value-prev_value*percent_difference)
        upper_threshold=int(prev_value+prev_value*percent_difference)
        return random.randint(lower_threshold,upper_threshold)

    def get_price(self, ticker):
        if ticker in self.tickers and 'price' in self.tickers[ticker]:
            prev_value=self.tickers[ticker]['price']
            new_value=self.get_next_value(prev_value)
            return {'timestamp': time.time(),'value':new_value}
        else:
            starting_price=self.get_starting_price()
            if ticker not in self.tickers:
                self.tickers[ticker]={}
            self.tickers[ticker]['price']=starting_price
            return {'timestamp': time.time(), 'value': starting_price}

    def get_indicator(self, ticker, indicator, start, end, params=[]):
        ret=[]
        if ticker in self.tickers and indicator in self.tickers[ticker]:
            prev_value=self.tickers[ticker][indicator]
            new_value=self.get_next_value(prev_value)
            ret.append({'timestamp': time.time(),'value':new_value})
        else:
            new_value=self.get_starting_price()
            if ticker not in self.tickers:
                self.tickers[ticker]={}
            self.tickers[ticker][indicator]=new_value
            ret.append({'timestamp': time.time(), 'value': new_value})
        return ret
