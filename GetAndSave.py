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
        print WrongMessage+'1'
    req=urllib2.Request(Url)
    try:
        reqopen=urllib2.urlopen(req)
    except:
        print WrongMessage+'2'
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
                print WrongMessage+'3'
            else:
                analysis=BeautifulSoup(Html)
                ana1=analysis.findAll('li')
                content=open(DataName,'a')
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
                            if ResNote.rfind(u'誠接各式自助套餐'.decode('utf-8'))==-1:
                                pass
                            else:
                                print ResNote
                        except:
                            ResNote=' '
                        try:
                            ResHour=ana2.find('p',attrs={'id':'hours'}).string.encode('utf-8')
                        except:
                            ResHour=' '
                        try:
                            ResAddress=ana2.find('p',attrs={'id':'address'}).string.encode('utf-8')
                        except:
                            ResAddress=' '
                        content.write(name.encode('utf-8')\
                                      +'@'+mainhost+RetMenu.encode('utf-8')\
                                      +'#'+ResTele[0:ResTele.rfind(u'&npsb;')].encode('utf-8')\
                                      +'%'+ResNote\
                                      +'&'+ResHour\
                                      +'*'+ResAddress\
                                      +'\n')
                content.close
    

testweb=mainhost+'/other/1'
GetAndSave(testweb)
print "finish"
