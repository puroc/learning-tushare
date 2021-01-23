# -*- coding:utf-8 -*- 
'''
Created on 2020年1月30日
@Group: waditu.com
@author: JM
'''

import pandas as pd
import lxml.html
from lxml import etree
from pymongo import MongoClient
import datetime

pd.set_option('display.max_colwidth', 20)
v = pd.__version__
from io import StringIO

# if int(v.split('.')[1])>=25:
#     from io import StringIO
# else:
#     from pandas.compat import StringIO
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

EXCHANGE_URLS = {
    #                  "DCE": ['http://www.dce.com.cn/dalianshangpin/yw/fw/jystz/ywtz/index.html', 'http://www.dce.com.cn', u'大商所'],
    #                  "SHFE": ['http://www.shfe.com.cn/news/notice/', 'http://www.shfe.com.cn', u'上期所'],
    "DONGFANG": [
        'http://reportapi.eastmoney.com/report/list?cb=datatable3724213&industryCode=*&pageSize=50&industry=*&rating=&ratingChange=&beginTime=2019-01-23&endTime=2021-01-23&pageNo=1&fields=&qType=0&orgCode=&code=601519%2C600111%2C000001%2C300999%2C000593%2C002475%2C600333%2C399006&rcode=&_=1611382695465',
        'http://www.shfe.com.cn', u'上期所'],
    #                  "CFFEX": ['http://www.cffex.com.cn/xwgg/jysgg/', 'http://www.cffex.com.cn/xwgg/jysgg/', u'中金所'],
    #                  "CZCE": ['http://www.czce.com.cn/portal/jysdt/ggytz/A090601index_1.htm', 'http://www.czce.com.cn', u'郑商所'],
}


def conteng_parse(exchange, uri):
    if exchange == 'DONGFANG':
        lines = get_content(EXCHANGE_URLS[exchange][1] + uri.strip())
        lines = lines.decode('utf-8')
        html = lxml.html.parse(StringIO(lines))
        res = html.xpath('//*[@id="stock_table"]/table/tbody/tr[1]/td[2]/a')
    elif exchange == 'CFFEX':
        uri = uri.strip()[1:]
        lines = get_content(EXCHANGE_URLS[exchange][1] + uri)
        html = lxml.html.parse(StringIO(lines))
        res = html.xpath('//div[@class=\"jysggright clearFloat\"]')
    elif exchange == 'DCE':
        lines = get_content(EXCHANGE_URLS[exchange][1] + uri)
        lines = _comps(lines)
        print(lines)
        html = lxml.html.parse(StringIO(lines))
        res = html.xpath('//div[@class=\"detail_inner\"]')
    else:
        pass
    if len(res) > 0:
        res = etree.tostring(res[0])
    #     res = res[0].xpath('string(.)') #取全部文字
    res = res.decode('utf8')
    if exchange == 'SHFE':
        res = res.replace('/upload/', EXCHANGE_URLS[exchange][1] + '/upload/')
    res = res.replace('<br>', '')
    res = res.replace('<p>', '')
    res = res.replace('</p>', '')
    res = res.replace('<br/>', '')
    res = res.replace('\n\n', '<br/>')
    res = res.replace('<br><br><br>', '')
    return res


def list_parse(exchange=None):
    print(exchange)
    lines = get_content(EXCHANGE_URLS[exchange][0])
    lines = lines.decode('utf8')
    lines = lines.replace("&", "&amp;")

    if exchange == 'DONGFANG':
        html = etree.HTML(lines)
        # res = html.xpath('/html/body/div[1]/div[8]/div[2]/div[6]')
        res = html.xpath('//*[@id="stock_table"]/table/tbody/tr')
        print(res)
        print(res)

    elif exchange == 'CFFEX':
        html = lxml.html.parse(StringIO(lines))
        res = html.xpath('//ul[@class=\"clearFloat\"]/li')
    elif exchange == 'DCE':
        lines = _comps(lines)
        html = lxml.html.parse(StringIO(lines))
        res = html.xpath('//ul[@class=\"list_tpye06\"]/li')
    else:
        lines = lines.decode('gbk')
        html = lxml.html.parse(StringIO(lines))
        res = html.xpath('//table[4]/tbody/tr[1]/td[4]/table[2]/tbody/tr[1]/td/table//tr')
    data = []
    if exchange == 'SHFE':
        for em in res:
            date = em.xpath('span/text()')[0]
            uri = em.xpath('a/@href')[0]
            title = em.xpath('a/text()')[0]
            content = conteng_parse(exchange, uri)
            data.append(
                [date.strip()[1:-1], EXCHANGE_URLS[exchange][1] + uri.strip(), title.strip(), content, exchange])
    elif exchange == 'CFFEX':
        for em in res:
            date = em.xpath('a[@class="time comparetime"]/text()')[0]
            uri = em.xpath('a[@class="list_a_text"]/@href')[0]
            title = em.xpath('a[@class="list_a_text"]/text()')[0]
            content = conteng_parse(exchange, uri)
            data.append(
                [date.strip()[1:-1], EXCHANGE_URLS[exchange][1] + uri.strip()[1:], title.strip(), content, exchange])
    elif exchange == 'DCE':
        for em in res:
            date = em.xpath('span/text()')[0]
            uri = em.xpath('a/@href')[0]
            title = em.xpath('a/text()')[0]
            content = conteng_parse(exchange, uri)
            data.append([date.strip(), EXCHANGE_URLS[exchange][1] + uri.strip(), title.strip(), content, exchange])
    else:
        for em in res:
            date = em.xpath('./td[2]')[0].xpath('string(.)')
            uri = em.xpath('./td[1]/a/@href')[0]
            title = em.xpath('./td[1]/a/text()')[0]
            #             content = conteng_parse(exchange, uri)
            url = EXCHANGE_URLS[exchange][1] + uri.strip()
            content = '[%s%s]%s<br><br><a href="%s">%s</a>' % (date, EXCHANGE_URLS[exchange][2], title, url, url)
            data.append([date.strip(), url, title.strip(), content, exchange])
    df = pd.DataFrame(data, columns=['date', 'url', 'title', 'content', 'exchange'])
    return df


def _comps(lines):
    try:
        import gzip
        cnt = StringIO(lines)
        gzipper = gzip.GzipFile(fileobj=cnt)
        lines = gzipper.read()
    except IOError:
        return lines
    return lines


def get_content(url):
    print(url)
    request = Request(url)
    request.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0')
    request.add_header("Connection", "keep-alive")
    request.add_header("Accept-Language", "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3")
    #     request.add_header("Accept-Encoding","gzip, deflate")
    #     request.add_header("Cookie", cookielib.CookieJar())
    text = urlopen(request, timeout=10).read()
    return text


if __name__ == '__main__':
    df = pd.DataFrame()
    for site in ['DONGFANG']:
        df = df.append(list_parse(site))
    print(df)
