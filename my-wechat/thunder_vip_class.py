# -*- coding:gb18030 -*-
import requests
from bs4 import BeautifulSoup

class Thunder_vip(object):
    """docstring for Thunder_vip"""
    def __init__(self, ):
        web=requests.get("http://www.loldytt.com/xunlei/vip/").content
        soup=BeautifulSoup(web,"html5lib")
        vipzuoce=soup.find_all("div")[23]
        p=vipzuoce.find_all("p")[0]
        self.vip_list=str(p)[5:-7].split("<br/>")

print Thunder_vip().vip_list[0]
