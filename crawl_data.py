from socket import  *
import sys
from lxml import etree
import time
import json
import urllib.request
import datetime,time
import csv
import re
def reportCraw():   #流动 速动
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0','Cookie':'Hm_lvt_1db88642e346389874251b5a1eded6e3=1554991041,1555140861,1555395453; device_id=0972d38fa0e01f14758734c6a9c2bf8b; s=e116dsm970; _ga=GA1.2.747460061.1555140852; xq_a_token=9557ecea528b70d977807513954308d48ded6dd6; xq_a_token.sig=KErZ9p0b5eAEagxuupMHrwQvF4s; xq_r_token=a175ca38aa6902e28e7e9ac289df3a3aa05ebe85; xq_r_token.sig=XEW1jYKHUWkS2SP8RuoHXO6Hhro; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1555397117; u=481555395452940'}
    x=[]
    data=[['股票代码','时间','开盘价','最高价','最低价','收盘价','涨跌幅','换手率']]
    orderT=[]
    allData=[]
    for i in range(1200):
        x.append(str(i+1).zfill(5))
    for z in x:
        url='http://emweb.securities.eastmoney.com/PC_HKF10/FinancialAnalysis/PageAjax?code='+z
        req=urllib.request.Request(url=url,headers=headers)
        content=urllib.request.urlopen(req).read()
        message = content.decode("utf8")
        flag=0
        ttmpData=[]
        if message == '{"msg":"股票代码不合法"}':
            print(z + 'error')
            continue
        else:
            rst = content.decode("utf-8")
            rst_dict = json.loads(rst)
            l=rst_dict['zcfzb']
            #l1=rst_dict['zyzb_abgq']  # 22净利率  1基本每股收益
            #print(l[0][22])
            #print(l[0][14]) #流动资产合计
            #print(l[0][44]) #流动负债合计

            if (l == [] or l[0][14] != '流动资产合计' or l[0][44] != '流动负债合计'):
                continue
            else:
                for i in range(1, len(l)):
                    if (l[i][14] == '--' or l[i][44] == '--'):
                        flag = 1
                        break
                    if l[i][14][-1] == '亿':
                        tmpNum = float(l[i][14][0:-1]) * 10000
                    elif l[i][14][-1] == '万':
                        tmpNum = float(l[i][14][0:-1])
                    else:
                        print('something wrong' + z)
                        tmpNum = float(l[i][14])
                        flag = 1
                        break

                    if l[i][44][-1] == '亿':
                        tmpNum1 = float(l[i][44][0:-1]) * 10000
                    elif l[i][44][-1] == '万':
                        tmpNum1 = float(l[i][44][0:-1])
                    else:
                        print('something wrong' + z)
                        tmpNum1 = float(l[i][44])
                        flag = 1
                        break

                    ttmpData.append([z, '20' + l[i][0][:5], float(tmpNum), float(tmpNum1)])
                if flag == 0:
                    for q in ttmpData:
                        allData.append(q)
                    print(z)
    return allData
def reportCraw1():   #财报数据 每股基本收益 净利率
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0','Cookie':'Hm_lvt_1db88642e346389874251b5a1eded6e3=1554991041,1555140861,1555395453; device_id=0972d38fa0e01f14758734c6a9c2bf8b; s=e116dsm970; _ga=GA1.2.747460061.1555140852; xq_a_token=9557ecea528b70d977807513954308d48ded6dd6; xq_a_token.sig=KErZ9p0b5eAEagxuupMHrwQvF4s; xq_r_token=a175ca38aa6902e28e7e9ac289df3a3aa05ebe85; xq_r_token.sig=XEW1jYKHUWkS2SP8RuoHXO6Hhro; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1555397117; u=481555395452940'}
    x=[]
    orderT=[]
    allData=[]
    for i in range(1200):
        x.append(str(i+1).zfill(5))
    for z in x:
        url='http://emweb.securities.eastmoney.com/PC_HKF10/FinancialAnalysis/PageAjax?code='+z
        req=urllib.request.Request(url=url,headers=headers)
        content=urllib.request.urlopen(req).read()
        message = content.decode("utf8")
        flag=0
        ttmpData=[]
        if message == '{"msg":"股票代码不合法"}':
            print(z + 'error')
            continue
        else:
            rst = content.decode("utf-8")
            rst_dict = json.loads(rst)
            l=rst_dict['zyzb_abgq']  # 22净利率  1基本每股收益
            #print(l[0][22])
            #print(l[0][14]) #流动资产合计
            #print(l[0][44]) #流动负债合计
            #print(l)
            if (l == [] or l[0][1] != '基本每股收益(元)' or l[0][22] != '净利率(%)'):
                continue
            else:
                for i in range(1, len(l)):
                    if (l[i][1] == '--' or l[i][22] == '--'):
                        flag = 1
                        break
                    ttmpData.append([z, '20' + l[i][0][:5], float(l[i][1]),float(l[i][22])])
                if flag == 0:
                    for q in ttmpData:
                        allData.append(q)
                    print(z)
    return allData
def combineReport():
    csv_file = csv.reader(open('reportData_asset.csv', 'r'))
    stock = []
    for i in csv_file:
        stock.append(i)
    csv_file = csv.reader(open('reportData_priceAndpro.csv', 'r'))
    price = []
    for i in csv_file:
        price.append(i)
    totalData=[['股票编号','报告日期','基本每股收益','净利率','流动比率','速动比率']]
    for i in price:
        flag = 0
        for j in stock:
            if j[0] == i[0] and j[1]==i[1]:
                totalData.append([j[0],j[1],i[2],i[3],j[2],j[3]])
                break
    return totalData
def dayData():
    csv_file=csv.reader(open('reportDataAll.csv','r'))
    report=[]
    for i in csv_file:
        report.append(i)
    print(report)
    returnData=[]
    for i in report:
        i[1]=i[1]+'-31'
    for i in range(1,len(report)-1):
        try:
            csv_file1=csv.reader(open('./stock data/'+report[i][0]+'.csv','r'))
            tmp=[]
            stock=[]
            for j in csv_file1:
                stock.append(j)
            del stock[0]
            flag=0
            for z in stock:
                if report[i][1]>=z[1] and report[i+1][1]<z[1]:
                    tmp.append(z[1:])
                    flag=1
            if flag==1:
                tmp.sort(key=lambda x:x[0],reverse=False)
                tmp.insert(0,report[i])
                returnData.append(tmp)
                print(report[i][0])
        except:
            print(report[i][0]+'error')
    return returnData
def dayDatadeal(): #统一序列长度
    csv_file=csv.reader(open('dayDataAll.csv','r'))
    data=[]
    for i in csv_file:
        for j in i:
            tmpData = re.findall(r"[\'](.*?)[\']", j)
            flag=1
            for z in tmpData:
                if z=='' or z=='--' or z=='Nan'or z=='nan' or z=='inf':
                    flag=0
            if flag==1:
                data.append(i)
    after=[]
    for i in data:
        if len(i)>121:
            length=len(i)
            for j in range(1,1+length-121):
                del i[1]
            after.append(i)
    return after
def lstmDataSet():
    csv_file = csv.reader(open('dayDataAfter.csv', 'r'))
    y=[]
    X=[]
    for i in csv_file:
        tmpData1 = re.findall(r"[\'](.*?)[\']", i[0])
        y.append([float(tmpData1[2])])
        tmp=[]
        for j in range(1,len(i)):
            tmpSecond=[]
            tmpData = re.findall(r"[\'](.*?)[\']", i[j])
            for z in range(1,len(tmpData)-2):
                tmpSecond.append(float(tmpData[z]))
            tmpSecond.append(float(tmpData[-2])/1000.0)
            tmpSecond.append(float(tmpData[-1]) / 100000.0)
            tmp.append(tmpSecond)
        X.append(tmp)
    train_X=[]
    train_y=[]
    test_X=[]
    test_y=[]
    for i in range(0,2500):
        train_X.append(X[i])
        train_y.append(y[i])
    for i in range(2500,3000):
        test_X.append(X[i])
        test_y.append(y[i])
    print('a')
def combineWave():
    csv_file = csv.reader(open('bpDataWave.csv', 'r'))
    csv_file1 = csv.reader(open('bpDataWithoutWave.csv', 'r'))
    all=[]
    for i in csv_file:
        all.append(i)
    for i in csv_file1:
        all.append(i)
    return all

def csv_in(str,data):
    with open(str, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)
        f.close()
all=combineWave()
csv_in('waveAll.csv',all)
