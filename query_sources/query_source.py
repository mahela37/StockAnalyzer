from providers.finhub import Api as indicator_api
from providers.yahoo import Api as price_volume_api

''' Inherit the methods from multiple providers. 
    This helps keep our code clean since we can instantiate one query source that is made of multiple API sources. 
'''
class Api(indicator_api,price_volume_api):
    def __init__(self):
        super(Api,self).__init__()
