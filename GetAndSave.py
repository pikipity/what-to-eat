# coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import os

mainhost='http://takeaway.happymacao.com'
DataName='test.txt'
WrongMessage=u"错误"

def GetAndSave(Url):
    try:
        os.remove(DataName)
    except:
        print WrongMessage
    req=urllib2.Request(Url)
    try:
        reqopen=urllib2.urlopen(req)
    except:
        print WrongMessage
    else:
        Html=reqopen.read()
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
                print WrongMessage
            else:
                analysis=BeautifulSoup(Html)
                ana1=analysis.findAll('div',attrs={'id':'name'})
                content=open(DataName,'a')
                for ana2 in ana1:
                    name=ana2.find('a').string
                    RetMenu=ana2.find('span',attrs={'id':'function'}).find('a')['href']
                    content.write(name.encode('utf-8')+'@'+mainhost+RetMenu.encode('utf-8')+'\n')
                content.close
    

testweb=mainhost+'/other/1'
GetAndSave(testweb)
print "finish"
