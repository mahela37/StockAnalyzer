import requests

''' Wrapper for the yahoo API '''
class Api():

    def __init__(self):
        pass

    def get_price_volume(self, ticker,start_timestamp,end_timestamp):    # Price and volume endpoint
        r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=CA&lang=en-CA&includePrePost=false&interval=1m&useYfid=true&range=1d&corsDomain=ca.finance.yahoo.com&.tsrc=finance')
        if (r.status_code != 200):  # Non-ok response
            return []
        result = r.json()
        timestamps = result['chart']['result'][0]['timestamp']
        prices = result['chart']['result'][0]['indicators']['quote'][0]['open']
        volume= result['chart']['result'][0]['indicators']['quote'][0]['volume']

        i=0
        return_array=[]
        for timestamp in timestamps:
            if timestamp <= start_timestamp:
                pass
            elif timestamp > end_timestamp:
                break
            else:   # Within range of specified time window
                return_array.append({'timestamp':timestamp,'price':prices[i],'volume':volume[i]})
            i=i+1
        return return_array
