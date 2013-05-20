# coding=utf-8
import Tkinter
import random
import time
import Queue
import threading
import os
import tkMessageBox
import win32api
from bs4 import BeautifulSoup
import urllib2

mainhost='http://takeaway.happymacao.com'
FileName='data\\set.txt'
WrongMessage=u"网络数据抓取错误，使用上次保留数据"

icon="icon\\eat.ico"

StartSwitch=Queue.Queue()
StartSwitch.put(0)

def GetAndSave(Url):
    req=urllib2.Request(Url)
    try:
        reqopen=urllib2.urlopen(req)
        Html=reqopen.read()
    except:
        Station.set(WrongMessage)
    else:
        analysis=BeautifulSoup(Html)
        PageNumber=analysis.find('span',attrs={'id':'pagenum'})
        AllWebPage=PageNumber.findAll('option')
        for WebPage in AllWebPage:
            Address=WebPage['value']
            req=urllib2.Request(Address)
            try:
                reqopen=urllib2.urlopen(req)
                Html=reqopen.read()
            except:
                Station.set(WrongMessage)
            else:
                analysis=BeautifulSoup(Html)
                ana1=analysis.findAll('div',attrs={'id':'name'})
                content=open(FileName,'a')
                for ana2 in ana1:
                    name=ana2.find('a').string
                    content.write(name.encode('utf-8')+'\n')
                content.close

def randomstring():
    Beginning=StartSwitch.get()
    StartSwitch.put(Beginning)
    Station.set(u"开始抓取网络数据")
    testweb=mainhost+'/other/1'
    GetAndSave(testweb)
    Station.set(u"抓取结束")
    fp=open(FileName,'r')
    lines=fp.readlines()
    fp.close()
    Station.set(u"点击停止随机抽取")
    while(Beginning==1):
        num=random.randrange(1,len(lines))
        Eating=lines[num]
        Eating=Eating[0:Eating.rfind("\n")]
        Eating=u"今天晚上吃  %s？"%Eating.decode('utf-8')
        Thing.set(Eating)
        time.sleep(0.1)
        Beginning=StartSwitch.get()
        StartSwitch.put(Beginning)
    NowEating=Thing.get()
    Station.set(u"抽取结束")
    Thing.set(NowEating[0:len(NowEating)-1]+u"!")
    

def Start():
    global StartorStop
    StartorStop=StartSwitch.get()
    StartSwitch.put(StartorStop)
    if(StartorStop==0):
        StartSwitch.get()
        StartSwitch.put(1)
        StartStop.set(u"停止")
        EatStart=threading.Thread(target=randomstring)
        EatStart.start()
    elif(StartorStop==1):
        StartSwitch.get()
        StartSwitch.put(0)
        StartStop.set(u"开始")

def SetWindow():
    Beginning=StartSwitch.get()
    StartSwitch.put(Beginning)
    if(Beginning==1):
        tkMessageBox.showwarning(u'呵呵',u"先停下好吗？")
    else:
        win32api.ShellExecute(0,'open','notepad.exe',FileName,'',1)

root=Tkinter.Tk()
root.title(u"今天晚上吃神马?")
root.iconbitmap(icon)

Thing=Tkinter.StringVar()
Thing.set(u"今天晚上吃神马？")
EatThing=Tkinter.Label(root,textvariable=Thing,font="Times,30,block",width=60)
EatThing.pack()

ButtonFrame=Tkinter.Frame(root)
ButtonFrame.pack()

StartStop=Tkinter.StringVar()
StartStop.set(u"开始")
StartButton=Tkinter.Button(ButtonFrame,command=Start,textvariable=StartStop,font="Times,15,block")
StartButton.pack(side="left")

SetButton=Tkinter.Button(ButtonFrame,text=u"设定",font="Times,15,block",command=SetWindow)
SetButton.pack(side="left")

Station=Tkinter.StringVar()
StationBar=Tkinter.Label(root,textvariable=Station,font="Times,5,block")
StationBar.pack()
Station.set(u"我是状态条")


root.mainloop()
