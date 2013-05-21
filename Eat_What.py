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

############## software information ########################
Version="1.0"
SoftwareName=u'今天晚上吃神马？'
############################################################

############# 常量 ###########################################
mainhost='http://takeaway.happymacao.com'
DataFile='data\\data.txt'
ConfigFile='data\\Config.txt'
WrongMessage=u"网络数据抓取错误，使用上次保留数据"

icon="icon\\eat.ico"

ThingDefault=u"今天晚上吃神马？"

StartButtonString_start=u"开始"
StartButtonString_stop=u"停止"

SettingButtonString=u"设定"

AboutButtonString=u"关于作者"

StationDefault=u'点击“开始”或按“回车”，开始随机抽取'
Station_After_Start=u'点击“停止”或按“回车”，结束随机抽取'
Station_After_Stop=u'抽取结束，点击餐厅名可以打开外卖单欧（需联网）'

Station_Setting_Before_Stop=u"先停下好吗？"

EatingNameDefault=u'仅提供 Takeaway Macao 上的餐厅'
EatingWebDefault=mainhost
EatingTeleDefault=u'有任何意见或建议可以联系我 -- pikipity'
EatingNoteDefault=u'我的联系方式：'
EatingHourDefault=u'pikipity@gmail.com'
EatingAddressDefault=u'pikipity.github.io'
###############################################################

########### 进程间传递参量 ######################################
StartSwitch=Queue.Queue(maxsize=1)
StartSwitch.put(0)

EatingWebStore=Queue.Queue(maxsize=1)
EatingWebStore.put(mainhost)
###############################################################

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
                ana1=analysis.findAll('li')
                content=open(DataFile,'a')
                for ana2 in ana1:
                    try:
                        name=ana2.find('span',attrs={'id':'name'}).find('a')\
                              .string
                    except:
                        pass
                    else:
                        RetMenu=ana2.find('span',attrs={'id':'function'})\
                                 .find('a')['href']
                        ResTele=ana2.find('p',attrs={'id':'tel'}).string
                        try:
                            ResNote=ana2.find('p',attrs={'id':'note'}).string.encode('utf-8')
                        except:
                            ResNote='         '
                        try:
                            ResHour=ana2.find('p',attrs={'id':'hours'}).string.encode('utf-8')
                        except:
                            ResHour='         '
                        try:
                            ResAddress=ana2.find('p',attrs={'id':'address'}).string.encode('utf-8')
                        except:
                            ResAddress=' '
                        # 书写格式：名字@菜单网址#电话%附注&营业时间*地址
                        content.write(name.encode('utf-8')\
                                      +'@'+mainhost+RetMenu.encode('utf-8')\
                                      +'#'+ResTele[0:ResTele.rfind(u'&npsb;')].encode('utf-8')\
                                      +'%'+ResNote\
                                      +'&'+ResHour\
                                      +'*'+ResAddress\
                                      +'\n')
                content.close

def GetResInfo():
    while(1):
        print "I am started"
        try:
            os.remove(DataFile)
        except:
            pass
        StartWeb=mainhost+'/other/1'
        GetAndSave_name(StartWeb)
        time.sleep(30)

def FirstReadDataFile():
    DataFileOK=0
    while(DataFileOK==0):
        Thing.set(u"稍等，下载数据中...")
        try:
            fp=open(DataFile,'r')
            lines=fp.readlines()
            fp.close()
        except:
            DataFileOK=0
        else:
            if len(lines)>=3:
                DataFileOK=1
            else:
                DataFileOK=0
    return lines

def ReadDataFile(Oddlines):
    try:
        fp=open(DataFile,'r')
        lines=fp.readlines()
        fp.close()
    except:
        lines=Oddlines
    else:
        if len(lines)>=3:
            pass
        else:
            lines=Oddlines
    return lines

def randomstring():
    Beginning=StartSwitch.get()
    StartSwitch.put(Beginning)
    lines=FirstReadDataFile()
    Station.set(Station_After_Start)
    while(Beginning==1):
        num=random.randrange(1,len(lines))
        Eating=lines[num]
        if Eating.rfind("@")==-1:
            pass
        else:
            EatingName=Eating[0:Eating.rfind("@")]
            EatingWeb=Eating[Eating.rfind("@")+1:Eating.rfind("#")]
            EatingTele=Eating[Eating.rfind("#")+1:Eating.rfind("%")]
            if Eating.rfind("&")==-1:
                EatingNext=lines[num+1]
                EatingNote=Eating[Eating.rfind("%")+1:Eating.rfind("\n")]\
                            +EatingNext[0:EatingNext.rfind("&")]
                EatingHour=EatingNext[EatingNext.rfind("&")+1:EatingNext.rfind("*")]
                EatingAddress=EatingNext[EatingNext.rfind("*")+1:EatingNext.rfind("\n")]
            else:
                EatingNote=Eating[Eating.rfind("%")+1:Eating.rfind("&")]
                EatingHour=Eating[Eating.rfind("&")+1:Eating.rfind("*")]
                EatingAddress=Eating[Eating.rfind("*")+1:Eating.rfind("\n")]
            EatingString=ThingDefault[0:4]+u" “%s”？"%EatingName.decode('utf-8')
            Thing.set(EatingString)
            time.sleep(0.1)
            lines=ReadDataFile(lines)
        Beginning=StartSwitch.get()
        StartSwitch.put(Beginning)
    NowEatingString=Thing.get()
    Thing.set(NowEatingString[0:len(NowEatingString)-1]+u"!")
    EatingNameVS.set(u'餐厅名：'+EatingName.decode('utf-8'))
    EatingWebVS.set(u'菜单：'+EatingWeb.decode('utf-8'))
    EatingWebStore.get()
    EatingWebStore.put(EatingWeb)
    EatingTeleVS.set(u'电话：'+EatingTele.decode('utf-8'))
    EatingNoteVS.set(u'注释：'+EatingNote.decode('utf-8'))
    EatingHourVS.set(u'营业时间：'+EatingHour.decode('utf-8'))
    EatingAddressVS.set(u'地址：'+EatingAddress.decode('utf-8'))
    Station.set(Station_After_Stop)


def OpenEatingWeb(event="None"):
    EatingWeb=EatingWebStore.get()
    EatingWebStore.put(EatingWeb)
    webbrowser.open(EatingWeb)
    

def Start(event="None"):
    global StartorStop
    StartorStop=StartSwitch.get()
    StartSwitch.put(StartorStop)
    if(StartorStop==0):
        StartSwitch.get()
        StartSwitch.put(1)
        StartStop.set(StartButtonString_stop)
        EatStart=threading.Thread(target=randomstring)
        EatStart.start()
    elif(StartorStop==1):
        StartSwitch.get()
        StartSwitch.put(0)
        StartStop.set(StartButtonString_start)

def SetWindow():
    Beginning=StartSwitch.get()
    StartSwitch.put(Beginning)
    if(Beginning==1):
        tkMessageBox.showwarning(u'呵呵',Station_Setting_Before_Stop)
    else:
        win32api.ShellExecute(0,'open','notepad.exe',DataFile,'',1)

        
def AboutFunction():
    AboutWin=Tkinter.Toplevel()
    AboutWin.iconbitmap(icon)
    AboutWin.title(AboutButtonString+' -- '+SoftwareName)
    TitleLabel=Tkinter.Label(AboutWin,text=SoftwareName,font="Times 30 bold",fg="#FF1493")
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
    

GetResInfoThreading=threading.Thread(target=GetResInfo)
GetResInfoThreading.start()

root=Tkinter.Tk()
root.title(SoftwareName)
root.iconbitmap(icon)
root.bind("<Return>",Start)

MainFrame=Tkinter.Frame(root)
MainFrame.pack()

##########################################################################
ControlFrame=Tkinter.Frame(MainFrame)
ControlFrame.pack()

Thing=Tkinter.StringVar()
Thing.set(ThingDefault)
EatThing=Tkinter.Label(ControlFrame,textvariable=Thing,font="Times,30,block",\
                       width=60,cursor="hand2")
EatThing.bind("<Button-1>",OpenEatingWeb)
EatThing.pack()

ButtonFrame=Tkinter.Frame(ControlFrame)
ButtonFrame.pack()

StartStop=Tkinter.StringVar()
StartStop.set(StartButtonString_start)
StartButton=Tkinter.Button(ButtonFrame,command=Start,textvariable=StartStop,font="Times,15,block")
StartButton.pack(side="left")

SetButton=Tkinter.Button(ButtonFrame\
                         ,text=SettingButtonString\
                         ,font="Times,15,block"\
                         ,command=SetWindow)
SetButton.pack(side="left")

AboutButton=Tkinter.Button(ButtonFrame\
                           ,text=AboutButtonString\
                           ,font="Times,15,block"\
                           ,command=AboutFunction)
AboutButton.pack(side="left")
##########################################################################

ContainFrame=Tkinter.Frame(MainFrame)
ContainFrame.pack()

EatingNameVS=Tkinter.StringVar()
EatingNameLabel=Tkinter.Label(ContainFrame,textvariable=EatingNameVS\
                              ,font="Times,10,block",cursor="hand2")
EatingNameLabel.bind("<Button-1>",OpenEatingWeb)
EatingNameLabel.pack()
EatingNameVS.set(EatingNameDefault)

EatingWebVS=Tkinter.StringVar()
EatingWebLabel=Tkinter.Label(ContainFrame,textvariable=EatingWebVS\
                             ,font="Times,10,block",cursor="hand2")
EatingWebLabel.bind("<Button-1>",OpenEatingWeb)
EatingWebLabel.pack()
EatingWebVS.set(EatingWebDefault)

EatingTeleVS=Tkinter.StringVar()
EatingTeleLabel=Tkinter.Label(ContainFrame,textvariable=EatingTeleVS,font="Times,10,block")
EatingTeleLabel.pack()
EatingTeleVS.set(EatingTeleDefault)

EatingNoteVS=Tkinter.StringVar()
EatingNoteLabel=Tkinter.Label(ContainFrame,textvariable=EatingNoteVS,font="Times,10,block")
EatingNoteLabel.pack()
EatingNoteVS.set(EatingNoteDefault)

EatingHourVS=Tkinter.StringVar()
EatingHourLabel=Tkinter.Label(ContainFrame,textvariable=EatingHourVS,font="Times,10,block")
EatingHourLabel.pack()
EatingHourVS.set(EatingHourDefault)

EatingAddressVS=Tkinter.StringVar()
EatingAddressLabel=Tkinter.Label(ContainFrame,textvariable=EatingAddressVS,font="Times,10,block")
EatingAddressLabel.pack()
EatingAddressVS.set(EatingAddressDefault)
##########################################################################

Station=Tkinter.StringVar()
StationBar=Tkinter.Label(root,textvariable=Station,font="Times,5,block")
StationBar.pack()
Station.set(StationDefault)

root.mainloop()
