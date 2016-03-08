# -*- coding:gb18030 -*-
import requests
from bs4 import BeautifulSoup

web=requests.get("http://www.loldytt.com/xunlei/vip/").content
soup=BeautifulSoup(web,"html5lib")
vipzuoce=soup.find_all("div")[23]
p=vipzuoce.find_all("p")[0]
p=str(p)[5:-7]
print p.replace("<br/>","\n")
a=input()
