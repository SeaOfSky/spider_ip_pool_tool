#-*-coding:utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import multiprocessing
import requests
from multiprocessing import Queue
import json


class ProxySpider(object):
    def __init__(self):
        pass
        
    
    def openPage(self):
#         response = urllib2.urlopen("http://www.xicidaili.com/nn/1")
        
        proxyurl = "http://www.xicidaili.com/nn/1"
        Headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }  
        request = urllib2.Request(url = proxyurl,headers = Headers)  
        response = urllib2.urlopen(request)  
        return response.read()
    
    def parse(self,html):
        soup = BeautifulSoup(html,"lxml")
        table_ip_list = soup.select('#ip_list')
        iplist = []
        i = 1
        for tbody in table_ip_list:
            for tr in tbody.select('tr'):
                if i:
                    i = 0 
                    continue
                ip = tr.contents[5].string
                port = tr.contents[7].string
                http = tr.contents[13].string
                if http == 'HTTP':
                    iplist.append((ip,port))
                    
        return iplist
    
    def start(self):
        page = self.openPage()
        iplist = self.parse(page)
        usefullist = []
        print "finish crawl proxy from http://www.xicidaili.com/nn/1"
        print "start to test proxy"
        
        return iplist;
#         for i in xrange(0,len(iplist)):
#             self.testproxy(iplist, i, usefullist)
#             print usefullist
#         print usefullist 
#         return usefullist
        
#         maxprocessnumber = 4
#         pool = multiprocessing.Pool(processes = maxprocessnumber)
#         for i in xrange(0,len(iplist)):
#             pool.apply_async(self.testproxy,(iplist,i,usefullist,))
#         pool.close()
#         pool.join()

#         usefullist = self.manager.list()
#         job = []
#         for i in xrange(0,len(iplist)):
#             p = multiprocessing.Process( target = testproxy, args = (iplist,i,usefullist,) )
#             p.start()
#             job.append(p)
#         for p in job:
#             p.join()
#         print usefullist

    
    
    def testproxy(self,iplist,index,usefullist=None):
        print index
        try:
            ipjson = {"http":"http://"+str(iplist[index][0])+":"+ str(iplist[index][1])}
            response = requests.get("http://www.baidu.com",proxies=ipjson)
            if "百度一下" not in response.content.decode("utf-8"):
                raise Exception
            else:
                print (iplist[index][0],iplist[index][1])
#                 usefullist.put((iplist[index][0],iplist[index][1]))
                return True
        except Exception,e:
            return False
                    
    
    def IsUseful(self,iplist):
        pass
        
def p(index,usefullist):
    print index
    print usefullist

def show(index,queue):
    queue.put(index)

def testproxy(ip,port,usefullist=None):
    print (ip,port)
    try:
        ipjson = {"http":"http://"+str(ip)+":"+ str(port)}
        response = requests.get("http://www.baidu.com",proxies=ipjson,timeout=3)
        usefullist.put((ip,port))
        return True
    except Exception,e:
        print e
        return False
    
if __name__ == "__main__":
    a = ProxySpider()
    iplist = a.start()
    
    manager = multiprocessing.Manager()
    q = manager.Queue()
    maxprocessnumber = 10
    pool = multiprocessing.Pool(processes = maxprocessnumber)
             
    for i in xrange(0,len(iplist)):
        ip = str(iplist[i][0])
        port = str(iplist[i][1])
        pool.apply_async(testproxy,(ip,port,q))
   
    pool.close()
    pool.join()
    
    print q.qsize()
#              
#     usefullist = a.manager.list()
#     queue = Queue()
#     job = []
#     usefullist = []
#     for i in xrange(0,20):
#         ip = str(iplist[i][0])
#         port = str(iplist[i][1])
#         p = multiprocessing.Process( target = testproxy, args = (ip,port) )
#         p.start()
#         job.append(p)
#     for p in job:
#         p.join()
#     print queue.qsize()