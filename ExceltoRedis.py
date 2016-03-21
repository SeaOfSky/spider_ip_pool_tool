#-*-coding:utf-8-*-
import redis
import xlrd,xlwt
import json
import urllib2
from bs4 import BeautifulSoup
import multiprocessing
import requests
from multiprocessing import Queue
import json
from __builtin__ import str

Redis_HOSt = "192.168.1.154"
Redis_PORT = "6379"
PROXY_KEY = "proxys"
S_ExcelPath = "proxy.xlsx"
D_ExcelPath = "m_proxy.xls"
MAX_PROCESS_NUMBER = 10
MAX_TEST_TIME_OUT = 4 


# multi testing proxy function
def testproxy(ip,port,category,usefullist=None):
    print (ip,port)
    try:
        ipjson = {category:category+"://"+str(ip)+":"+ str(port)}
        response = requests.get("http://www.baidu.com",proxies=ipjson,timeout=MAX_TEST_TIME_OUT)
        usefullist.put((ip,port,category))
        return True
    except Exception,e:
        print e
        return False
    
def multitask(iplist,q):
    pool = multiprocessing.Pool(processes = MAX_PROCESS_NUMBER)
             
    for i in xrange(0,len(iplist)):
        ip = str(iplist[i][0])
        port = str(iplist[i][1])
        category = str(iplist[i][2])
        pool.apply_async(testproxy,(ip,port,category,q))
   
    pool.close()
    pool.join()

def ReadFromExcel(excel_path):
    NeedData = []
    data = xlrd.open_workbook(excel_path)
    table = data.sheets()[0]
    for i in xrange(1,table.nrows):
        NeedData.append(table.row_values(i))
    
    return NeedData

def transfertojson(ip,port,category):
    JsonProxy = {"ip":str(ip),"port":int(port),"category":str(category).lower()}  
    return json.dumps(JsonProxy)

def committoRedis(key,content):
    server = redis.Redis(Redis_HOSt, Redis_PORT)
    return server.sadd(key,content)

def writetoExcel(q):
    w = xlwt.Workbook()
    ws = w.add_sheet('sheet 1')
    for i in xrange(0,q.qsize()):
        row = q.get()   
        ws.write(i,0, row[0])
        ws.write(i,1, row[1])
        ws.write(i,2, row[2])
    w.save(D_ExcelPath)


#after testing ,write proxy data to redis
def start():
    print "Read from excel:" + str(S_ExcelPath)
    data = ReadFromExcel(S_ExcelPath)
    iplist = []
    for row in data:
        iplist.append((row[0], row[1], str(row[4]).lower()))
        
    print "finshi reading. size:" + str(len(iplist))
    print "starting test proxy..."
    
    manager = multiprocessing.Manager()
    q = manager.Queue()
    multitask(iplist,q)
    print "finish testing. qsize:" + str(q.qsize())
    writetoExcel(q)
    
    
#directly wirte excel data to redis
def worker():
    server = redis.Redis(Redis_HOSt, Redis_PORT)
    data = ReadFromExcel(D_ExcelPath)
    for row in data:
        json = transfertojson(row[0], row[1], row[2])
        if server.sadd(PROXY_KEY,json):
            print str(row[0])+str(row[1])+str(row[2])+"  succcess"
        else:
            print str(row[0])+str(row[1])+str(row[2])+"  failed!"
            
if __name__ == "__main__":
    cmd = raw_input("Input A Index(1.test proxy or 2.write to redis  3. all(1 and 2)):")
    if cmd == "1":
        start()
    elif cmd == "2":
        worker()
    elif cmd == "3":
        start()
        worker()
