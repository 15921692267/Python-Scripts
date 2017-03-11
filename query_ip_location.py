#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import sys
import urllib
from bs4 import BeautifulSoup
import re

def queryIpLocation(ip):
    res = urllib.urlopen("http://ip138.com/ips1388.asp?ip=%s&action=2" %(ip))
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')
    li_element = str(soup.li)     # 查询结果一行是li元素，而且其他地方没有
    m = re.search(r"<li>.*：(.*) (.*) (.*)</li>", li_element) 
    location = m.group(1)
    company = m.group(2)
    isp = m.group(3)
    if location:
        print("地理位置: %s" % location)
    if company:
        print("公司名: %s" % company)
    if isp:
        print("服务商: %s" % isp)

if __name__ == "__main__":
    ip = sys.argv[1]
    queryIpLocation(ip)