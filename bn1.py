import datetime

import openpyxl
import pandas as pd

### BANK NIFTY BUY and SELL strategy
## Time Frame Should be 30 Min
      ## FOR BUY STRATEGY ##
## 1st and 2nd Candle should be green i.e: 1stcandle Close greater than 1st candle Open and
                                        ## 2nd Candle Close greater than 2nd candle open
##2nd candle High should be entry point and should be break in 3rd candle only
## Stop loss should be 2nd candle low
## Target is 1:1

       ## FOR SELL STRATEGY ##
## 1st and 2nd Candle should be red i.e: 1stcandle Close less than 1st candle Open and
                                        ## 2nd Candle Close less than 2nd candle open
##2nd candle low should be entry point and should be break in 3rd candle only
## Stop loss should be 2nd candle high
## Target is 1:1

f_list = []
df_cols = ["LTP", 'Times']
df = pd.read_csv(str(datetime.date.today()) + 'bn.csv', names=df_cols, index_col=1, parse_dates=True)
df.reset_index(inplace=True)
df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
# df['Times']=pd.to_datetime(df['Times'], unit='s')
df.set_index('Times', inplace=True)
## Converting tick data to 30 min
df = df['LTP'].resample('30min', base=15).ohlc().dropna()
# df=df.drop_duplicates(inplace=False)
print((df))

if (float(df.iloc[[1]]['close']) < float(df.iloc[[1]]['open']) and
      float(df.iloc[[2]]['close']) < float(df.iloc[[2]]['open']) and
      float(df.iloc[[2]]['low']) < float(df.iloc[[1]]['low'])):

    print('Bank Nifty Future Sell Recommanded Price is  :', float(df.iloc[[2]]['low'] - 2))
    points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    print('Bank Nifty Future buy target is :', float(df.iloc[[2]]['low']) - points)
    print('Bank Nifty Future stoploss is :', float(df.iloc[[2]]['high']))
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('SELL')
    f_list.append(float(df.iloc[[2]]['low'] - 2))
    f_list.append(float(float(df.iloc[[2]]['low']) - points))
    f_list.append(float(df.iloc[[2]]['high']))


## 1st and 2nd Candle should be green i.e: 1stcandle Close greater than 1st candle Open and
                                        ## 2nd Candle Close greater than 2nd candle open
elif (float(df.iloc[[1]]['close']) > float(df.iloc[[1]]['open']) and
      float(df.iloc[[2]]['close']) > float(df.iloc[[2]]['open']) and
      float(df.iloc[[2]]['high']) > float(df.iloc[[1]]['high'])):
    ##2nd candle High should be entry point and should be break in 3rd candle only
    print('Bank Nifty Future Buy Recommanded Price is  :', float(df.iloc[[2]]['high'] + 2))
    points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    print('Bank Nifty Future sell target is :', float(df.iloc[[2]]['low']) + points)
    ## Stop loss should be 2nd candle low
    print('bank Nifty Future stoploss is :', float(df.iloc[[2]]['low']))
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('BUY')
    f_list.append(float(df.iloc[[2]]['high'] + 2))
    f_list.append(float(float(df.iloc[[2]]['high']) + points))
    f_list.append(float(df.iloc[[2]]['low']))

book = openpyxl.load_workbook('bank_results.xlsx')
sheet = book.active

sheet.append(f_list)
book.save('bank_results.xlsx')
