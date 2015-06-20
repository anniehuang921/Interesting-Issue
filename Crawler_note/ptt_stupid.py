#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
import requests
import os
url="https://www.ptt.cc/bbs/StupidClown/index.html"
ptt="https://www.ptt.cc"
from pyquery import PyQuery
import re
def rec(R):#R=S1('div.r-ent')
    c=[]
    for i in R:
        S2=PyQuery(i)
        if  len(S2('div.nrec span'))!=0 and S2('div.title a').text()!="":
            if S2('div.nrec span')[0].text == u'爆':
                    if filter(lambda x: x in S2('div.title a').text(),[u"[問卷]",u"[集氣]"])==[]:
                        c.append(S2)
    return c
def three(R):
    """
    Where site R putting url. 
    """
    c=[]
    res=requests.get(R)
    s=PyQuery(res.text)
    S=s('div.pull-right a.btn:nth-child(2)')
    T=S.attr('href')
    p=re.compile("\d{4}")
    t=p.search(S.attr('href'))
    page=t.group()
    T=T.replace(page,str(int(page)+2))
    page=str(int(page)+2)
    while len(c)<5:
        T=T.replace(page,str(int(page)-1))
        M=ptt+T
        Res2=requests.get(M)
        S3=PyQuery(Res2.text)
        
        K=rec(S3('div.r-ent'))
        c.extend(K)
        page=str(int(page)-1)
        #c=c[:5]
    SS1="<!DOCTYPE html><html><header><meta charset=\"utf-8\"/></header><body>"
    SS2=[]
    for i in c:
        SS2.append("<a style=\"font-size:40px\" href=\""+ptt+i('div.title a').attr('href')+"\">"+i('div.title a').text()+"</a>"+"</br>")
    SS3="</h1></body></html>"
    SS=SS1
    for i in range(len(c)):
        SS+=SS2[i]
    SS=SS+SS3
    f=open("foo.html","w")
    print >>f,SS.encode('utf-8')
    f.close()
    return c
three(url)
import time
import random
r= random.randint(0,5)
time.sleep(r)

os.system("open foo.html")