# -*- coding: utf-8 -*-

import tushare as ts


# 上市公司信息
from db.BaseSql import base_insert
from db.GlobalDB import StockDb


class StockInfo(object):

    def __init__(self):
        self.ts = ts.pro_api('a1a2a46baa4b687e1f1a2237412c643e29ce247350a0d80100f0bfca')

    def stocks(self):
        stocks_list = self.ts.stock_basic(exchange='', list_status='L',
                                          fields='ts_code,symbol,name,fullname,market,'
                                                 'area,list_status,industry,list_date,'
                                                 'delist_date,is_hs')
        for index, stock in stocks_list.iterrows():
            stock_info = dict()
            stock_info['ts_code'] = stock['ts_code']
            stock_info['name'] = stock['name']
            stock_info['full_name'] = stock['fullname']
            stock_info['market'] = stock['market']
            stock_info['list_status'] = stock['list_status']
            stock_info['list_date'] = stock['list_date']
            stock_info['is_hs'] = stock['is_hs']
            base_insert(stock_info, 'stocks', StockDb)


if __name__ == '__main__':
    StockInfo().stocks()
