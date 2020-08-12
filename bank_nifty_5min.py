import datetime
import openpyxl
import pandas as pd



f_list = []
df_cols = ["LTP", 'Times']
df = pd.read_csv(str(datetime.date.today()) + 'bn.csv', names=df_cols, index_col=1, parse_dates=True)
df.reset_index(inplace=True)
df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
# df['Times']=pd.to_datetime(df['Times'], unit='s')
df.set_index('Times', inplace=True)
## Converting tick data to 30 min
df = df['LTP'].resample('5min', base=15).ohlc().dropna()
# df=df.drop_duplicates(inplace=False)
print((df))

# Continous last Seven candels are Close less than Open (RED)
if (float(df.iloc[[-1]]['close']) < float(df.iloc[[-1]]['open']) and
        float(df.iloc[[-2]]['close']) < float(df.iloc[[-2]]['open']) and
        float(df.iloc[[-3]]['close']) < float(df.iloc[[-3]]['open']) and
        float(df.iloc[[-4]]['close']) < float(df.iloc[[-4]]['open']) and
        float(df.iloc[[-5]]['close']) < float(df.iloc[[-5]]['open']) and
        float(df.iloc[[-6]]['close']) < float(df.iloc[[-6]]['open']) and
        float(df.iloc[[-7]]['close']) < float(df.iloc[[-7]]['open'])):

    # Low of the last seven Candles
    print('Bank Nifty Future Sell Recommanded Price is  :', float(min(df.iloc[-1:-8:-1]['low'])))
    #points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    #print('Bank Nifty Future buy target is :', float(df.iloc[[2]]['low']) - points)
    # Previous candle of  Low of the last seven Candles high
    print('Bank Nifty Future stoploss is :', df.iloc[(df.iloc[-1:-8:-1]['low'].idxmin())-1]['high'])
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('SELL')
    f_list.append(float(min(df.iloc[-1:-8:-1]['low'])))
    #f_list.append(float(float(df.iloc[[2]]['low']) - points))
    f_list.append(float(df.iloc[(df.iloc[-1:-8:-1]['low'].idxmin())-1]['low']))
    # #print(zebu_api.place_bracket_order('NFO',44329, 'BANKNIFTY20AUGFUT', 'bo', 'SELL', 'DAY', float(df.iloc[[2]]['low'] - 2), 'L', '25',
    # (float(df.iloc[[2]]['low']) - points), float(df.iloc[[2]]['high']), 5))


# Continous last Seven candels in CLOSE greater than OPEN (GREEN)
elif (float(df.iloc[[-1]]['close']) > float(df.iloc[[-1]]['open']) and
        float(df.iloc[[-2]]['close']) > float(df.iloc[[-2]]['open']) and
        float(df.iloc[[-3]]['close']) > float(df.iloc[[-3]]['open']) and
        float(df.iloc[[-4]]['close']) > float(df.iloc[[-4]]['open']) and
        float(df.iloc[[-5]]['close']) > float(df.iloc[[-5]]['open']) and
        float(df.iloc[[-6]]['close']) > float(df.iloc[[-6]]['open']) and
        float(df.iloc[[-7]]['close']) > float(df.iloc[[-7]]['open'])):
    ##2nd candle High should be entry point and should be break in 3rd candle only
    print('Bank Nifty Future Buy Recommanded Price is  :', float(max(df.iloc[-1:-8:-1]['high'])))
    #points = float(df.iloc[[2]]['high'] - df.iloc[[2]]['low'])
    #print('Bank Nifty Future sell target is :', float(df.iloc[[2]]['low']) + points)
    ## Stop loss should be 2nd candle low
    # Previous candle of  high of the last seven Candles low
    print('bank Nifty Future stoploss is :', df.iloc[(df.iloc[-1:-8:-1]['high'].idxmin())-1]['low'])
    f_list.append(datetime.date.today())
    f_list.append('BANK NIFTY')
    f_list.append('BUY')
    f_list.append(float(max(df.iloc[-1:-8:-1]['high'])))
    #f_list.append(float(float(df.iloc[[2]]['high']) + points))
    f_list.append(df.iloc[(df.iloc[-1:-8:-1]['high'].idxmin())-1]['low'])
    # #print(zebu_api.place_bracket_order('NFO',44329, 'BANKNIFTY20AUGFUT', 'bo', 'BUY', 'DAY', float(df.iloc[[2]]['high'] + 2), 'L', '25',
    # (float(float(df.iloc[[2]]['high']) + points), float(df.iloc[[2]]['low']), 5))

book = openpyxl.load_workbook('bank_nifty_5min_results.xlsx')
sheet = book.active

sheet.append(f_list)
book.save('bank_results.xlsx')
