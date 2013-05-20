# coding=utf-8
import Tkinter
import string
import random
import time
import Queue
import threading
import os
import tkMessageBox
import win32api
from bs4 import BeautifulSoup
import urllib2
import webbrowser

Version="1.0"
SoftwareName=u'今天晚上吃神马？'

mainhost='http://takeaway.happymacao.com'
DataFile='data\\data.txt'
ConfigFile='data\\Config.txt'
WrongMessage=u"网络数据抓取错误，使用上次保留数据"

icon="icon\\eat.ico"

StartSwitch=Queue.Queue(maxsize=1)
StartSwitch.put(0)

EatingWebStore=Queue.Queue(maxsize=1)
EatingWebStore.put(mainhost)

def GetAndSave_name(Url):
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
                content=open(DataFile,'a')
                for ana2 in ana1:
                    name=ana2.find('a').string
                    RetMenu=ana2.find('span',attrs={'id':'function'}).find('a')['href']
                    content.write(name.encode('utf-8')+'@'+mainhost+RetMenu.encode('utf-8')+'\n')
                content.close

def randomstring():
    Beginning=StartSwitch.get()
    StartSwitch.put(Beginning)
    Config=open(ConfigFile,'r')
    Configure=Config.readlines()
    Config.close()
    ConfigUpdata=Configure[0]
    ConfigUpdataState=ConfigUpdata[ConfigUpdata.rfind(" ")+1:len(ConfigUpdata)]
    if ConfigUpdataState=='ToUpdata':
        Station.set(u"开始抓取网络数据")
        try:
            os.remove(DataFile)
        except:
            Station.set(u"没有这个文件，准备创建新Data.txt文件")
        testweb=mainhost+'/other/1'
        GetAndSave_name(testweb)
        Configure[0]=string.replace(ConfigUpdata,'ToUpdata','Updata')
        Config=open(ConfigFile,'w')
        Config.writelines(Configure)
        Config.close()
        Station.set(u"抓取结束")
    fp=open(DataFile,'r')
    lines=fp.readlines()
    fp.close()
    Station.set(u'点击“停止”，结束随机抽取')
    while(Beginning==1):
        num=random.randrange(1,len(lines))
        Eating=lines[num]
        EatingName=Eating[0:Eating.rfind("@")]
        EatingWeb=Eating[Eating.rfind("@")+1:Eating.rfind("/n")]
        EatingString=u"今天晚上吃 “%s”？"%EatingName.decode('utf-8')
        Thing.set(EatingString)
        time.sleep(0.1)
        Beginning=StartSwitch.get()
        StartSwitch.put(Beginning)
    NowEatingString=Thing.get()
    Thing.set(NowEatingString[0:len(NowEatingString)-1]+u"!")
    EatingWebStore.get()
    EatingWebStore.put(EatingWeb)
    Station.set(u'抽取结束，点击餐厅名可以显示外卖单欧')


def OpenEatingWeb(event="None"):
    EatingWeb=EatingWebStore.get()
    EatingWebStore.put(EatingWeb)
    webbrowser.open(EatingWeb)
    

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
        win32api.ShellExecute(0,'open','notepad.exe',DataFile,'',1)

        
def AboutFunction():
    AboutWin=Tkinter.Toplevel()
    AboutWin.iconbitmap(icon)
    AboutWin.title(u'关于作者'+' -- '+SoftwareName)
    TitleLabel=Tkinter.Label(AboutWin,text="Speaking",font="Times 30 bold",fg="#FF1493")
    TitleLabel.pack()
    VersionLabel=Tkinter.Label(AboutWin,text="Version "+Version,\
                               font="Times 15 bold")
    VersionLabel.pack()
    WriteLabel=Tkinter.Label(AboutWin,text="Writed by pikipity",\
                             font="Times 17 bold",fg="#008FFF")
    WriteLabel.pack()
    EmailLabel=Tkinter.Label(AboutWin,text="pikipity's emal: pikipityw@gmail.com",\
                            font="Times 17 bold",fg="#008FFF")
    EmailLabel.pack()
    BlogLabel=Tkinter.Label(AboutWin,text="pikipity's blog: pikipity.github.io",\
                            font="Times 17 bold",fg="#008FFF",cursor="hand2")
    BlogLabel.bind("<Button-1>",OpenBlog)
    BlogLabel.pack()
def OpenBlog(event="None"):
    webbrowser.open("pikipity.github.io")
    

root=Tkinter.Tk()
root.title(SoftwareName)
root.iconbitmap(icon)

Thing=Tkinter.StringVar()
Thing.set(u"今天晚上吃神马？")
EatThing=Tkinter.Label(root,textvariable=Thing,font="Times,30,block",width=60,cursor="hand2")
EatThing.bind("<Button-1>",OpenEatingWeb)
EatThing.pack()

ButtonFrame=Tkinter.Frame(root)
ButtonFrame.pack()

StartStop=Tkinter.StringVar()
StartStop.set(u"开始")
StartButton=Tkinter.Button(ButtonFrame,command=Start,textvariable=StartStop,font="Times,15,block")
StartButton.pack(side="left")

SetButton=Tkinter.Button(ButtonFrame,text=u"设定",font="Times,15,block",command=SetWindow)
SetButton.pack(side="left")

AboutButton=Tkinter.Button(ButtonFrame,text=u'关于作者',font="Times,15,block",command=AboutFunction)
AboutButton.pack(side="left")

Station=Tkinter.StringVar()
StationBar=Tkinter.Label(root,textvariable=Station,font="Times,5,block")
StationBar.pack()
Station.set(u'点击“开始”，开始随机抽取')


root.mainloop()
