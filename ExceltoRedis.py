import redis
import xlrd
import json

Redis_HOSt = "192.168.1.154"
Redis_PORT = "6379"
ExcelPath = "proxy.xlsx"
PROXY_KEY = "proxys"

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

def worker():
    server = redis.Redis(Redis_HOSt, Redis_PORT)
    data = ReadFromExcel(ExcelPath)
    for row in data:
        json = transfertojson(row[0], row[1], row[4])
        if server.sadd(PROXY_KEY,json):
            print str(row[0])+str(row[1])+str(row[4])+"  succcess"
        else:
            print str(row[0])+str(row[1])+str(row[4])+"  failed!"
            
if __name__ == "__main__":
    worker()
