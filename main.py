import os,time
from services.finhub import Api
import components.stock as stock

query_source = Api()

with open('stocks.txt') as f:
    list_stocks=f.readlines()

start=time.time()

stocks=stock.Stocks(list_stocks, query_source)
stocks.refresh()


end=time.time()
print(end-start)

