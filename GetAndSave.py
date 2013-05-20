# coding=utf-8

from bs4 import BeautifulSoup
import urllib2

mainhost='http://takeaway.happymacao.com'
FileName='test.txt'
WrongMessage=u"错误"

def GetAndSave(Url):
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
            except:
                print WrongMessage
            else:
                Html=reqopen.read()
                analysis=BeautifulSoup(Html)
                ana1=analysis.findAll('div',attrs={'id':'name'})
                content=open(FileName,'a')
                for ana2 in ana1:
                    name=ana2.find('a').string
                    content.write(name.encode('utf-8')+'\n')
                content.close
    

testweb=mainhost+'/other/1'
GetAndSave(testweb)
print "finish"
