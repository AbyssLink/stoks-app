import json
import os
import time
from os import path

import akshare as ak
import pandas as pd
import yfinance as yf


class StockHelper:
    def __init__(self, symbol: str):
        super().__init__()
        self.__symbol = symbol
        self.__stock_df = self.get_remote_data()

    def get_remote_data(self):
        if not path.exists('static'):
            os.mkdir('static')
        wiret_path = path.join('static', f'{self.__symbol}_history.csv')
        if(path.exists(wiret_path)):
            # fetch file every day
            if (time.time() - path.getmtime(wiret_path)) <= float(24*60*60):
                with open(wiret_path) as f:
                    print(f'fetch local data = {self.__symbol}_history.csv')
                    stock_us_df = pd.read_csv(
                        f, index_col='date', parse_dates=True)
                    return stock_us_df
        try:
            stock_us_df = ak.stock_us_daily(symbol=self.__symbol)
            stock_us_df.to_csv(wiret_path)
            print('fetch remote data = akshare')
            return stock_us_df
        except KeyError as e:
            return None

    def get_stock_df(self):
        return self.__stock_df

    def get_recent_chart_data(self):
        if self.__stock_df is not None:
            stock_data = []
            for i, j in self.__stock_df.tail(80).iterrows():
                stock_data.append({'x': i.strftime('%b %d'), 'y': [
                                  j['open'], j['high'], j['low'], j['close']]})
            return stock_data
        else:
            return {'success': False}

    def get_rencent_list_data(self):
        if self.__stock_df is not None:
            stock_data = []
            for i, j in self.__stock_df.tail(80).iterrows():
                stock_data.append({'symbol': self.__symbol,
                                   'time': i.strftime('%Y-%m-%d'),
                                   'open': j['open'], 'high': j['high'], 'low': j['low'],
                                   'close': j['close'], 'volume': j['volume']
                                   })
            # return reversed list
            return stock_data[::-1]
        else:
            return {'success': False}

    def get_factor_data(self):
        qfq_df = ak.stock_us_daily(symbol=self.__symbol, factor="qfq")
        print(qfq_df)

    def get_stock_info(self):
        if self.__stock_df is not None:
            if not path.exists('static'):
                os.mkdir('static')
            wirte_path = path.join('static', f'{self.__symbol}.json')
            if(path.exists(wirte_path)):
                with open(wirte_path, 'r') as f:
                    stock_info = json.loads(f.read())
                    print(f'fectch local info = {self.__symbol}.json')
            else:
                stock = yf.Ticker(self.__symbol)
                try:
                    stock_info = stock.info
                    print(f'fectch remote info = {self.__symbol}.json')
                    with open(path.join('static', f'{self.__symbol}.json'), 'w') as fp:
                        json.dump(stock_info, fp)
                except IndexError:
                    return {'success': False}
            res = dict((k, stock_info[k]) for k in ["logo_url", "sector", "phone", "website", "fullTimeEmployees"]
                       if k in stock_info)
            # print(res)
            return res
        else:
            return {'success': False}

    def test(self):
        stock_us_df = ak.stock_us_daily(symbol='AAPL')


if __name__ == '__main__':
    sh = StockHelper('TSLA')
    # sh.get_factor_data()
    sh.get_stock_info()
