#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import re
import requests
import urllib
from bs4 import BeautifulSoup
import base64

class Search_movies(object):
    """docstring for Search_movies"""
    def __init__(self, keyword):
        keyword=unicode(keyword)
        self.keyword = keyword.encode("gbk")
        self.keyword=urllib.quote(self.keyword)
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        data={
                'typeid':2,
                'keyword':"%s" % self.keyword,
                'Input':urllib.unquote("%CB%D1%CB%F7"),
        }
        #result=requests.post("http://www.4567.tv/search.asp",headers=headers,data=data).content.decode("gbk","ignore")
        result=requests.get("http://www.4567.tv/search.asp?keyword=%s"% self.keyword,headers=headers).content.decode("gbk","ignore")
        #print re.findall("<li>.+?<em>(.+)?</em>.+?<a href=\"(.+)?\" title</li>",result)
        soup=BeautifulSoup(result,"html5lib")
        movies_list_link=soup.find_all("li")[5:]
        self.movie_information={}
        self.movie_list=[]
        movie=movies_list_link[0]
        #for movie in movies_list_link:
        self.movie_information={}
        self.movie_information["url"]="http://www.4567.tv"+movie.a["href"]
        self.movie_information["title"]=movie.a["title"]
        self.movie_list.append(self.movie_information)
        for movie in self.movie_list:
            url=movie["url"]
            result=requests.get(url,headers=headers).content
            soup=BeautifulSoup(result,"html5lib")
            script=soup.find_all("script")[15].text
            #country=soup.find_all("li")[3].text[-3:]
            #date=soup.find_all("li")[4].text[5:]
            movie_name=soup.find_all("h1")[0].text
            download_url=script
            download_url=re.findall('''"(.+)?"''',download_url,re.S)
            try:
                download_url=download_url[0].split("###")
            except:
                pass
            movie["download_url"]=download_url
            #movie["country"]=country
            #movie["date"]=date
            movie["name"]=movie_name
if __name__=="__main__":
    c=raw_input(":")
    a=Search_movies(c)
    print a.movie_list
    print a.movie_list[0]["name"]

