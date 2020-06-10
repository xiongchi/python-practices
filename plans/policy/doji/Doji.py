# -*- coding: utf-8 -*-
# 十字星策略
from db.GlobalDB import StockDb


class Doji(object):

    def __init__(self):
        pass

    def analyse(self, trade_date):
        daily_price_sql = "select * from daily_data where trade_date = %s"
        now_trades = StockDb.getAll(daily_price_sql, (trade_date,))
        stocks = []
        for trade in now_trades:
            ts_code = trade['ts_code']
            if not ts_code.startswith('3'):
                stock_info = StockDb.getOne("select * from stocks where ts_code = %s", (ts_code,))
                if stock_info is None:
                    continue
                if stock_info['name'].find('ST') != -1:
                    continue
                high = trade['high']
                low = trade['low']
                open = trade['open']
                close = trade['close']
                pre_close = trade['pre_close']
                amplitude = abs((high - low)/pre_close * 100)
                compute = (open - close)/open * 100
                if amplitude > 2.0:
                    if -0.5 < compute < 0.5:
                        before_trade = self.before_trade_date(ts_code, '20200609')
                        pct_chg = before_trade['pct_chg']
                        if pct_chg < -2.0:
                            if open < 50:
                                stocks.append(ts_code)
                                print(ts_code)

    def before_trade_date(self, ts_code, before_date):
        before_date_sql = "select * from daily_data where ts_code = %s and trade_date = %s"
        before_trade = StockDb.getOne(before_date_sql, (ts_code, before_date))
        return before_trade


if __name__ == '__main__':
    Doji().analyse('20200610')