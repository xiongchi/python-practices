# -*- coding: utf-8 -*-
# 日线行情数据
import datetime

import tushare as ts

from db.BaseSql import base_insert
from db.GlobalDB import StockDb


class DailyDate(object):

    def __init__(self):
        self.ts = ts.pro_api('a1a2a46baa4b687e1f1a2237412c643e29ce247350a0d80100f0bfca')

    def dailyPrice(self, date_str):
        daily_data = self.ts.daily(trade_date=date_str)
        for index, data in daily_data.iterrows():
            hq = dict()
            hq['ts_code'] = data['ts_code']
            hq['trade_date'] = data['trade_date']
            hq['open'] = data['open']
            hq['high'] = data['high']
            hq['low'] = data['low']
            hq['close'] = data['close']
            hq['pre_close'] = data['pre_close']
            hq['change'] = data['change']
            hq['pct_chg'] = data['pct_chg']
            hq['vol'] = data['vol']
            hq['amount'] = data['amount']
            print(hq)
            base_insert(hq, 'daily_data', StockDb)

    def historyData(self):
        for i in range(365):
            date = datetime.datetime.now() - datetime.timedelta(days=i)
            date_str = date.strftime('%Y%m%d')
            self.dailyPrice(date_str)


if __name__ == '__main__':
    # DailyDate().historyData()
    DailyDate().dailyPrice('20200610')