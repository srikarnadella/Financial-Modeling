api_key = 'CFWLTRA3PQVFVFCI'

import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time


ticker = input("What stock do you want analysis on (ticker)? ")
ts = TimeSeries(key = api_key, output_format = 'pandas')
data, meta_data = ts.get_intraday(symbol = ticker, interval = '1min', outputsize = 'full')
print(data)

i = 1
while i == 1:
    data, meta_data = ts.get_intraday(symbol = ticker, interval = '1min', outputsize = 'full')
    data.to_excel("output.xlsx")
    time.sleep(60)

close_data = data['4. close']
percentchange = close_data.pct_change()

print(percentchange)
last_change = percentchange[-1]
if abs(last_change) > 0.004:
    print("{ticker} Alert: " + last_change)