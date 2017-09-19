# -*- coding: utf-8 -*-
"""
Created on Sun Jul 09 21:22:46 2017

@author: QY
"""
import time
import random
#import urllib
import urllib2

import requests
import bs4

from bs4 import BeautifulSoup

import xlwt
import xlrd
from xlutils.copy import copy


proxys=('111.155.116.249:8123',
        '182.92.242.11:80',
        '111.155.116.220:8123',
        '110.73.0.233:8123',
        '113.200.214.164:9999',
        '218.56.132.157:8080',
        '118.178.124.33:3128',
        '120.132.71.212:80',
        '222.33.192.238:8118')

def getHtml(url):
    while 1==1:
        
        #i=random.randint(0,9)
        i=0
        if i==0:
            page=urllib2.urlopen(url)
            html=page.read()
            print "local"
            return html
            break
        try:
            requests.get('http://www.baidu.com',proxies={"http":proxys[i]})
        except:
            continue
        else:
            proxy={'http':proxys[i]}
            print proxy['http']
            proxy_handler=urllib2.ProxyHandler(proxy)
            opener=urllib2.build_opener(proxy_handler)
            
            urllib2.install_opener(opener)
            response=urllib2.urlopen(url)
            html=response.read()
            return html
            break

#html=getHtml("http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=23&tableName=TABLE23&tableView=GMP%E8%AE%A4%E8%AF%81&Id=2000000")
count=0
num=1
while num<10:
    try:
        url='http://qy1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=国产药品&Id='+str(num)
        print url; 
        time.sleep(1.5);
        html=getHtml(url)       
        time.sleep(2.5)
        print "HTML READY"
        soup=BeautifulSoup(html);
        a=soup.select('td')[2].get_text().strip()
        
        if a==u'没有相关信息':
            print '404';
            num+=1;
            continue;
    
        medic_ratify=soup.select('td')[2].get_text().strip();
        medic_name=soup.select('td')[4].get_text().strip();
        medic_name_EN=soup.select('td')[6].get_text().strip();
        medic_name_mer=soup.select('td')[8].get_text().strip();
        medic_type=soup.select('td')[10].get_text().strip();
        medic_norm=soup.select('td')[12].get_text().strip();
        medic_factory=soup.select('td')[14].get_text().strip();
        medic_factory_address=soup.select('td')[16].get_text().strip();
        medic_category=soup.select('td')[18].get_text().strip();
        medic_ratify_date=soup.select('td')[20].get_text().strip();
        medic_ratify_original=soup.select('td')[22].get_text().strip();
        medic_number=soup.select('td')[24].get_text().strip();
        medic_number_remark=soup.select('td')[26].get_text().strip();
        medic_relateDB=soup.select('td')[28].get_text().strip();
        medic_other=soup.select('td')[32].get_text().strip();
        '''
        print medic_ratify
        print medic_name
        print medic_name_EN
        print medic_name_mer
        print medic_type
        print medic_norm
        print medic_factory
        print medic_factory_address
        print medic_category
        print medic_ratify_date
        print medic_ratify_original
        print medic_number
        print medic_number_remark
        print medic_relateDB
        print medic_other
        '''
        rb=xlrd.open_workbook("medic1-10.xls")
        wb=copy(rb)
        ws=wb.get_sheet(0)
        ws.write(count,0,num)
        ws.write(count,1,medic_ratify)
        ws.write(count,2,medic_name)
        ws.write(count,3,medic_name_EN)
        ws.write(count,4,medic_name_mer)
        ws.write(count,5,medic_type)
        ws.write(count,6,medic_norm)
        ws.write(count,7,medic_factory)
        ws.write(count,8,medic_factory_address)
        ws.write(count,9,medic_category)
        ws.write(count,10,medic_ratify_date)
        ws.write(count,11,medic_ratify_original)
        ws.write(count,12,medic_number)
        ws.write(count,13,medic_number_remark)
        ws.write(count,14,medic_relateDB)
        ws.write(count,15,medic_other)
              
        wb.save("medic1-10.xls")
        
        time.sleep(0.5)
    except BaseException:
        continue
    else:
        num+=1
        count+=1
        print 'success'
        
'''
wb=xlwt.Workbook()
ws=wb.add_sheet('Sheet1')
ws.write(0,0,'test')
wb.save("D:\\text.xlsx")
'''
