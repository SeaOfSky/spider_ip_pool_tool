#-*-coding:utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import multiprocessing
import requests
from multiprocessing import Queue
import json
import xlwt


D_ExcelPath = "test.xls"

class ProxySpider(object):
    def __init__(self):
        pass
        
    
    def openPage(self,proxyurl):
#         response = urllib2.urlopen("http://www.xicidaili.com/nn/1")
        Headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }  
        request = urllib2.Request(url = proxyurl,headers = Headers)  
        response = urllib2.urlopen(request)  
        return response.read()
    
    def parse(self,html,iplist):
        soup = BeautifulSoup(html,"lxml")
        table_ip_list = soup.select('#ip_list')
        i = 1
        for tbody in table_ip_list:
            for tr in tbody.select('tr'):
                if i:
                    i = 0 
                    continue
                ip = tr.contents[5].string
                port = tr.contents[7].string
                http = tr.contents[13].string
                iplist.append((ip,port,str(http).lower()))
    
    def start(self):
        iplist = []
        proxyurl = "http://www.xicidaili.com/nn/"
        for i in xrange(1,10):
            page = self.openPage( proxyurl +str(i))
            self.parse(page,iplist)
            
        self.writetoExcel(iplist)
    
    def writetoExcel(self,iplist):
        w = xlwt.Workbook()
        ws = w.add_sheet('sheet 1')
        for i in xrange(0,len(iplist)):
            ws.write(i,0, iplist[i][0])
            ws.write(i,1, iplist[i][1])
            ws.write(i,4, iplist[i][2])
            w.save(D_ExcelPath)
    
if __name__ == "__main__":
    a = ProxySpider()
    iplist = a.start()