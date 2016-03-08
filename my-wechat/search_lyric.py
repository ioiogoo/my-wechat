#-*-:coding:utf-8 -*-
import requests
import urllib
import json
import re

class search_lyric(object):
    def __init__(self, keyword):
        #keyword=urllib.quote(keyword)
        self.keyword=keyword
        params='?aggr=0&catZhida=1&lossless=0&sem=1&w=%s&n=4&t=7&p=1&searchid=103947064867995831&remoteplace=txt.yqqlist.lyric&g_tk=5381&loginUin=0&hostUin=0&format=jsonp&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&jsonpCallback=searchJsonCallback&needNewCode=0' % self.keyword
        result=requests.get("http://soso.music.qq.com/fcgi-bin/search_cp"+ params).content
        result_json=result[19:-1]
        result_dic=json.loads(result_json)["data"]
        lyric_dic=result_dic['lyric']
        #totalnum=lyric_dic['totalnum']
        #curpage=lyric_dic['curpage']
        lyric_list=lyric_dic['list']
        self.songname=lyric_list[0]['songname']
        self.songmid=lyric_list[0]["songmid"]
        self.singer=lyric_list[0]['singer'][0]['name']
        self.content=lyric_list[0]['content'].replace("br/",'\n').replace("&lt;","").replace("&gt;","").replace("strong class=&quot;keyword&quot;","").replace("/strong","")
        self.content= "".join(re.split(r"&#\d+;",self.content))
        try:
            self.songurl=lyric_list[0]["songurl"]
        except:pass
if __name__=="__main__":
    Content="CXGC 宠爱"
    if Content.split(" ")[0]=="CXGC":      #判断为“歌词查询”
                Content=Content[4:].replace(" ","")
                try:
                    result=search_lyric(Content)
                    Content=result.songname+"\n"+result.content
                    try:
                        Content=Content+"\n"+result.songmid
                    except:
                        pass
                except :
                    Content="未找到歌曲，请重试！"
    print Content

