import datetime

import pandas as pd
from nsepy import get_history


class MYCUSTOMUTILS():

    def excel_to_csv(self, file_path, index_name, save_loc):
        df = pd.read_excel(file_path)
        df.reset_index()
        df.set_index(index_name, inplace=True)
        df.to_csv(save_loc)
        return "Sucessfully completed"

    def resample_csv_to_dataframe(self, file_path, resample, base=0, df_cols=['LTP', 'Times']):
        df = pd.read_csv(file_path, names=df_cols, index_col=1, parse_dates=True)
        df.reset_index(inplace=True)
        df['Times'] = [datetime.datetime.fromtimestamp(x) for x in df['Times']]
        df.set_index('Times', inplace=True)
        df = df['LTP'].resample(resample, base).ohlc().dropna()
        return df

    def get_history_of_stock(self, symbol, start_date='2020,1,1', end_date=datetime.date.today()):
        data = get_history(symbol=symbol, start=datetime.date(start_date), end=end_date)
        return data


a = MYCUSTOMUTILS()
print(MYCUSTOMUTILS.get_history_of_stock('CIPLA'))
