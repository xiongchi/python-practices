import tushare as ts


def stock_Info():
    pro = ts.pro_api('a1a2a46baa4b687e1f1a2237412c643e29ce247350a0d80100f0bfca')
    data = pro.stock_basic(exchange='', list_status='L',
                           fields='ts_code,symbol,name,area,industry,list_date')
    df = pro.daily(ts_code='000001.SZ', start_date='20200601', end_date='20206004')
    # df = pro.daily(trade_date='20200810')
    print(data)


if __name__ == '__main__':
    stock_Info()