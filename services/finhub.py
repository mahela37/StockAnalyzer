import requests
import config
class Api():

    config=None
    tokens=None
    token_length=0
    token = ''
    index=0
    max_poll_rate=0

    def __init__(self):
        self.config=config.config
        self.tokens=self.config['api']['finhub']['tokens']
        self.token_length=len(self.tokens)
        self.max_poll_rate=self.config['api']['finhub']['max_poll_rate']

    def rotate_token(self):
        if(self.index==self.token_length):
            self.index=0

        self.token=self.tokens[self.index]
        self.index = self.index + 1

    def get_price(self, ticker):
        self.rotate_token()
        r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={self.token}')
        if (r.status_code != 200):
            return None
        result = r.json()
        if "p" not in result or "t" not in result:
            return None
        return {'timestamp': result['t'], 'value': result['p']}

    def get_indicator(self, ticker, indicator, start, end, params=[]):
        self.rotate_token()
        base_string = f'https://finnhub.io/api/v1/indicator?symbol={ticker}&resolution=1&from={start}&to={end}&indicator={indicator}&token={self.token}'

        for key in params:
            base_string = base_string + f'&{key}={params[key]}'

        r = requests.get(base_string)
        data = r.json()

        if (r.status_code != 200):
            return None

        val = data[indicator]
        time = data['t']
        ret = []
        for i, entry in enumerate(val):
            ret.append({'timestamp': time[i], 'value': entry})
        return ret
