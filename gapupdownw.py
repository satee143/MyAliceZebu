import datetime

import openpyxl
import pandas as pd

## Read Previous Day Low and High

df_cols = ["DayHigh", 'DayLow']
pre_df = pd.read_csv('gapupdown.csv', names=df_cols, index_col=1, parse_dates=True)
pre_df.reset_index(inplace=True)
print(pre_df.iloc[0]['DayHigh'])
print(pre_df.iloc[0]['DayLow'])

# Read Ticker Data
f_list = []
df_cols = ["LTP", 'Times']
df = pd.read_csv(str(datetime.date.today()) + '.csv', names=df_cols, index_col=1, parse_dates=True)
df.reset_index(inplace=True)
df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
# df['Times']=pd.to_datetime(df['Times'], unit='s')
df.set_index('Times', inplace=True)
df = df['LTP'].resample('15min').ohlc().dropna()
# df=df.drop_duplicates(inplace=False)
print((df))

### Nifty Should Be Opened GAP UP/GAP DOWN
## Trade Should be executed 09-30 to 09-45 only
## If GAP UP 1st Candle High  is Entry , StopLoss is 1st Candle Low and Target is 1:1
## If GAP DOWN 1st Candle Low is Entry,  StopLoss is 1st Candle High and Target is 1:1 or 1:2

if (float(df.iloc[[1]]['open']) > float(pre_df.iloc[0]['DayHigh'])):
    print('Nifty Future Buy Recommanded Price is  :', float(df.iloc[[1]]['high']))
    points = float(df.iloc[[1]]['high'] - df.iloc[[1]]['low'])
    print('Nifty Future Sell target is :', float(df.iloc[[1]]['high']) + points)
    print('Nifty Future stoploss (Sell) is :', float(df.iloc[[1]]['low']))
    f_list.append(datetime.date.today())
    f_list.append('NIFTY')
    f_list.append('BUY')
    f_list.append(float(df.iloc[[1]]['high']))
    f_list.append(float(float(df.iloc[[1]]['high']) + points))
    f_list.append(float(df.iloc[[1]]['low']))
    # zebu_api.place_bracket_order('NFO','NIFTYJUL20FUT','BO','BUY','DAY',10300,'l',75,10400,10200,20,)

## If GAP DOWN 1st Candle Low is Entry,  StopLoss is 1st Candle High and Target is 1:1 or 1:2
elif (float(df.iloc[[1]]['open']) < float(pre_df.iloc[0]['DayLow'])):
    print('Nifty Future Sell Recommanded Price is  :', float(df.iloc[[1]]['low']))
    points = float(df.iloc[[1]]['high'] - float(df.iloc[[1]]['low']))
    print(points)
    print('Nifty Future Buy target is :', float(df.iloc[[1]]['low']) - points)
    print('Nifty Future stoploss (Buy) is :', float(df.iloc[[1]]['high']))
    f_list.append(str(datetime.date.today()))
    f_list.append('NIFTY')
    f_list.append('SELL')
    f_list.append(float(df.iloc[[1]]['low']))
    f_list.append(float(float(df.iloc[[1]]['low']) - points))
    f_list.append(float(df.iloc[[1]]['high']))

book = openpyxl.load_workbook('gapup.xlsx')
sheet = book.active
sheet.append(f_list)
book.save('gapup.xlsx')
