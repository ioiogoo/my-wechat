#-*- coding:utf-8 -*-
from flask import Flask,make_response,render_template,redirect,url_for,session,flash,request
from flask.ext.bootstrap import Bootstrap
from form import LoginForm,RegisterForm
from flask.ext.sqlalchemy import SQLAlchemy
import os,hashlib
import xml.etree.ElementTree as ET
from  search_lyric import search_lyric
import time
import re

app=Flask(__name__)
db=SQLAlchemy(app)
bootstrap=Bootstrap(app)

app.config["SECRET_KEY"]="myname is hefeng"
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///"+os.path.join(basedir,"data.db")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True

class Role(db.Model):
    __tablename__="roles"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    def __repr__(self):
        return "<Role %r>" % self.name
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    user=db.Column(db.String(64),unique=True,index=True)
    password=db.Column(db.String)
    def __repr__(self):
        return "<User %r>" % self.name
@app.route("/")
def index():
    name=session.get("name")
    return render_template("index.html",name=name)

@app.route("/login",methods=["GET","POST"])
def login_in():
    form=LoginForm()
    user=form.name.data
    password=form.password.data
    if form.validate_on_submit():
        if user=="ioiogoo" and password=="1":
            session["name"]=form.name.data
            return redirect(url_for("index"))
        flash("password false!")
        return redirect(url_for("login_in"))
    return render_template("login.html",form=form)

@app.route("/login_out")
def login_out():
    session["name"]=None

@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        name=form.name.data
        password=form.password.data
        user=User.query.filter_by(user=name).first()
        if user is None:
            user=User(user=name,password=password)
            db.session.add(user)
            db.session.commit()
            session["name"]=form.name.data
            return render_template("index.html",name=name)
        else:
            return redirect(url_for("login_in"))
    return render_template("register.html",form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.route("/weixin",methods=["GET","POST"])
def wechat():
    if request.method == 'GET':
        token = 'ioiogoo'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if ( hashlib.sha1(s).hexdigest() == signature ):
          return make_response(echostr)
    xml_recv = ET.fromstring(request.data)
    ToUserName = xml_recv.find("ToUserName").text
    FromUserName = xml_recv.find("FromUserName").text
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    try:#----------------------判断是否第一次关注
        Event=xml_recv.find("Event").text
        len(Event)!=0
        if re.match("subscribe",Event):
            Content="欢迎订阅此公众号，随时随地查找歌曲。\n功能介绍：\n1）查询歌词：\n 支持通过歌曲名、歌词或者歌手名查找歌曲，并且可以在线试听 \n例如：需要查找《浏阳河》这首歌的歌词，可以发送：\n CXGC 浏阳河\n CXGC 弯过了几道弯 \n CXGC 沙宝亮 \n查找到《浏阳河》这首歌 \n2）福利查询：\n本订阅号会不定时地给大家发送福利，大家可以通过发送：FLFS（福利放送）查询 \n3）大家如果任何建议请直接发送：JY+内容。如果你有更加好玩的点子，记得告诉我哟\n更多功能还在开发中，敬请期待吧！"
        #-----------------------判断关注结束
    except:#接受消息
        Content = xml_recv.find("Content").text
        if Content[0:4]=="CXGC":      #判断为“歌词查询”
            try:
                Content=Content[4:]
                result=search_lyric(Content)
                Content="%s\n%s" % (result.songname,result.content)
                try:
                    wenzi=u"点击这里试听"
                    Content=Content+"\n"+"<a href=\"http://i.y.qq.com/s.plcloud/fcgi-bin/fcg_yqq_song_detail_info_cp.fcg?songmid=%s\">%s</a>" % (result.songmid,wenzi)
                except:
                    pass
            except :
                Content="未找到歌曲，请重试！"
        #------------------------------判断"歌词查询"结束
        elif Content[0:4]=="FLFS":
            Content='''敬请期待，谢谢！
            '''
        else:
            Content='''请按以下格式发送消息：\n查询歌词：CXGC+空格+内容\n福利发送：FLSF\n更多功能还在开发中。。。'''
    response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())),Content ) )   #回复消息格式
    response.content_type = 'application/xml'
    return response
if __name__=="__main__":
    app.run(debug=True)
