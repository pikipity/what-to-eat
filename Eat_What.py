# coding=gbk
import Tkinter
import random
import time
import Queue
import threading
import os
import tkMessageBox
import win32api

StartSwitch=Queue.Queue()
StartSwitch.put(0)

fp=open("data\\set.txt",'r')
lines=fp.readlines()
fp.close()

def randomstring():
    Beginning=StartSwitch.get()
    StartSwitch.put(Beginning)
    fp=open("data\\set.txt",'r')
    lines=fp.readlines()
    fp.close()
    while(Beginning==1):
        num=random.randrange(1,len(lines))
        Eating=lines[num]
        Eating=Eating.decode('gb2312')
        Eating=Eating[0:Eating.rfind("\n")]
        Eating=u"今天晚上吃"+Eating+u"?"
        Thing.set(Eating)
        time.sleep(0.1)
        Beginning=StartSwitch.get()
        StartSwitch.put(Beginning)
    NowEating=Thing.get()
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
        tkMessageBox.showwarning('HeHe',u"先停下好吗？")
    else:
        win32api.ShellExecute(0,'open','notepad.exe','data\\set.txt','',1)

root=Tkinter.Tk()
root.title(u"今天晚上吃神马?")
root.iconbitmap("icon\\eat.ico")

Thing=Tkinter.StringVar()
Thing.set(u"今天晚上吃神马？")
EatThing=Tkinter.Label(root,textvariable=Thing,font="Times,20,block",width=60)
EatThing.pack()

ButtonFrame=Tkinter.Frame(root)
ButtonFrame.pack()

StartStop=Tkinter.StringVar()
StartStop.set(u"开始")
StartButton=Tkinter.Button(ButtonFrame,command=Start,textvariable=StartStop,font="Times,15,block")
StartButton.pack(side="left")

SetButton=Tkinter.Button(ButtonFrame,text=u"设定",font="Times,15,block",command=SetWindow)
SetButton.pack(side="left")


root.mainloop()
