#!/usr/bin/env python3.5
# -*- coding:utf8 -*-
import time,os
import asyncio
import aiohttp
# 十档行情
class Leverfun:
    stock_api = 'https://app.leverfun.com/timelyInfo/timelyOrderForm'
    def __init__(self):
        self.stocks_dict = dict()
    def stocks(self, stock_codes):
        if type(stock_codes) is not list:
            stock_codes = [stock_codes]
        threads = []
        for stock in stock_codes:
            threads.append(self.get_stock_detail(stock))
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(threads))
        return self.stocks_dict
    async def get_stock_detail(self, stock_code):
        params = dict(stockCode=stock_code)
        async with aiohttp.get(Leverfun.stock_api, params=params) as r:
            r_json = await r.json()
            self.stocks_dict[stock_code] = Leverfun.format_response_data(r_json)
    @classmethod
    def format_response_data(cls, response_data, **kwargs):
        data = response_data['data']
        buys = data['buyPankou']
        sells = data['sellPankou']
        stock_dict = dict(
            close=round(data['preClose'], 3),
            now=data['match'],
            buy=buys[0]['price'],
            sell=sells[0]['price'],
        )
        for trade_info_li, name in zip([sells, buys], ['ask', 'bid']):
            for i, trade_info in enumerate(trade_info_li):
                stock_dict['{name}{index}'.format(name=name, index=i + 1)] = trade_info['price']
                stock_dict['{name}{index}_volume'.format(name=name, index=i + 1)] = trade_info['volume'] * 100
        return stock_dict
if __name__ == "__main__":
    code = ""
    if code == "":
        code = input("请输入代码：")
    if code:
        # 实例化十档行情
        q = Leverfun()
        while True:
            # d_sina = quotaion_sina(code)
            d_lf = q.stocks(code)
            os.system("cls")
            mydata = """
    现价：%s 元
    卖十价：%s   卖十量：%s 手    买十价：%s   买十量：%s 手
    卖九价：%s   卖九量：%s 手    买九价：%s   买九量：%s 手
    卖八价：%s   卖八量：%s 手    买八价：%s   买八量：%s 手
    卖七价：%s   卖七量：%s 手    买七价：%s   买七量：%s 手
    卖六价：%s   卖六量：%s 手    买六价：%s   买六量：%s 手
    卖五价：%s   卖五量：%s 手    买五价：%s   买五量：%s 手
    卖四价：%s   卖四量：%s 手    买四价：%s   买四量：%s 手
    卖三价：%s   卖三量：%s 手    买三价：%s   买三量：%s 手
    卖二价：%s   卖二量：%s 手    买二价：%s   买二量：%s 手
    卖一价：%s   卖一量：%s 手    买一价：%s   买一量：%s 手
    """ %(d_lf[code]['now'],d_lf[code]['ask10'],d_lf[code]['ask10_volume']/100,d_lf[code]['bid10'],d_lf[code]['bid10_volume']/100,
d_lf[code]['ask9'],d_lf[code]['ask9_volume']/100,d_lf[code]['bid9'],d_lf[code]['bid9_volume']/100,
d_lf[code]['ask8'],d_lf[code]['ask8_volume']/100,d_lf[code]['bid8'],d_lf[code]['bid8_volume']/100,
d_lf[code]['ask7'],d_lf[code]['ask7_volume']/100,d_lf[code]['bid7'],d_lf[code]['bid7_volume']/100,
d_lf[code]['ask6'],d_lf[code]['ask6_volume']/100,d_lf[code]['bid6'],d_lf[code]['bid6_volume']/100,
d_lf[code]['ask5'],d_lf[code]['ask5_volume']/100,d_lf[code]['bid5'],d_lf[code]['bid5_volume']/100,
d_lf[code]['ask4'],d_lf[code]['ask4_volume']/100,d_lf[code]['bid4'],d_lf[code]['bid4_volume']/100,
d_lf[code]['ask3'],d_lf[code]['ask3_volume']/100,d_lf[code]['bid3'],d_lf[code]['bid3_volume']/100,
d_lf[code]['ask2'],d_lf[code]['ask2_volume']/100,d_lf[code]['bid2'],d_lf[code]['bid2_volume']/100,
d_lf[code]['ask1'],d_lf[code]['ask1_volume']/100,d_lf[code]['bid1'],d_lf[code]['bid1_volume']/100,
)
            print(mydata)
            time.sleep(3)