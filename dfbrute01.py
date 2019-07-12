#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
@Author: fragrant
'''
from fake_useragent import UserAgent
import requests, sys, os, time, threading, urllib, pyfiglet, terminal_banner

# For Print
longSpace = '                                 '


# 随机ua
def headersRandom():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    return headers

# 读文件 url集合 和字典
def readFile(fileName, lineNum, dictFileName, blackResLen, lastTenResLen):
    with open(fileName, 'r') as file:
        url = file.readlines()[lineNum].strip()
        print('-- scanning -- {0}'.format(url))
        readDictFileAndBrute(url, dictFileName, blackResLen, lastTenResLen)
        # return url


# 读
# TODO 多次返回一样可能是有问题
def readDictFileAndBrute(url, dictFileName, blackResLen, lastTenResLen):
    with open(dictFileName, 'r') as file:
        for line in file:
            urlNew = url + line.strip()
            # print(urlNew)
            try:
                res = requests.get(urlNew, headers=headersRandom(), timeout=50)
                # time.sleep(0.5)
                # print(res.request.headers)
                # print(res.status_code)
                if res.history and res.status_code in [301, 302]:
                    for is301302403405401 in res.history:
                        if is301302403405401.status_code in [301, 302]:
                            print('[+] %s -> %s (CODE: %s -> CODE: %s |SIZE:%s)' % (urlNew, urllib.parse.unquote(res.url, encoding='utf-8', errors='replace') ,is301302403405401.status_code, res.status_code, len(res.text)), end="\n")
                # print(res.history)
                # print(res.url)
                elif res.status_code in [200, 403, 405]:
                    if len(lastTenResLen) < 10:
                        lastTenResLen.append(len(res.text))
                        if len(res.text) not in blackResLen:
                            # 前10个都会输出 并且不会生成黑名单
                            print('[+] %s (CODE: %s|SIZE:%s)' % (urlNew, res.status_code, len(res.text)))
                    elif len(lastTenResLen) == 10:
                        del lastTenResLen[0]
                        lastTenResLen.append(len(res.text))
                        # print(len(lastTenResLen), end='\n\n')
                        # print(blackResLen)
                        lastTenIsSameOrNot = len(list(set(lastTenResLen)))
                        # 如果连续10个都是返回值一样并且不在黑名单里面那就说明是有问题的返回
                        if lastTenIsSameOrNot == 1 and len(res.text) not in blackResLen:
                            blackResLen.append(len(res.text))
                            print('1[-] %s (CODE: %s|BLACKSIZE: %s) %s' % (urlNew, res.status_code, len(res.text), longSpace), end='\r')
                        elif len(res.text) in blackResLen:
                            print('2[-] %s (CODE: %s|SIZE: %s) %s' % (urlNew, res.status_code, len(res.text), longSpace), end='\r')
                        elif lastTenIsSameOrNot != 1 and len(res.text) not in blackResLen:
                            print('[+] %s (CODE: %s|SIZE: %s)' % (urlNew, res.status_code, len(res.text)))
                else:
                    print('[-] %s (CODE: %s|SIZE:%s)%s' % (urlNew, res.status_code, len(res.text), longSpace), end='\r')
                    # print('res.status_code {0}'.format())
            except Exception as error:
                # time.sleep(300)
                print('[X] URL: ' + urlNew + ' length: ' + 'None ' + 'Error: ' , error)

def usage():
    f = pyfiglet.Figlet(font="3-d")
    print(f.renderText("dfbrute"))
        # curentFileName = os.path.basename(sys.argv[0])
        # print('Usage: python3 ' + curentFileName + ' http://url OR https://url' + ' worldList')
    print('''\
--------------------------
dfbrute v1.0
by fragrant
github https://github.com/fragrant10/dfbrute
--------------------------

Usage:
 python3 dfbrute01.py <url OR urls> worldList 2

EXAMPLES:
 python3 dfbrute01.py http://baidu.com/ worldList 2
 python3 dfbrute01.py https://baidu.com/ worldList 2
 python3 dfbrute01.py urlsFile worldList 2''')

def main():
    if len(sys.argv) > 1:
        # urls 域名文件
        # dictFileName 字典文件
        # threadNum 线程数
        urls = sys.argv[1]
        dictFileName = sys.argv[2]
        threadNum = sys.argv[3]
        # 如果传入的是链接或者urls域名文件
        if urls[:4] == 'http':
            url = sys.argv[1]
            readDictFileAndBrute(url, dictFileName, blackResLen, lastTenResLen)
        elif os.path.exists(urls):
            urlsLines = len(open(urls,'rU').readlines())    # 域名文件有多少行
            print(urlsLines)
            readedUrlLine = 0   # 已经读取过的url行数
            while True:
                # 响应黑名单 在扯个列表里面的长度值不再打印 因为可能是waf 
                blackResLen = []
                # 如果最后10次请求的响应值一样那么就判定 可能有waf 加入黑名单不再打印
                lastTenResLen = []
                urlsLines -= int(threadNum) # 域名文件还剩多少行 为了防止ip被封 每个线程只分配一个url进行扫描
                if urlsLines >= 0:
                    readedUrlLine += int(threadNum) # 记录读过的行数
                    theadObjThreads = [] # 线程列表
                    for lineNum in range(readedUrlLine-int(threadNum), readedUrlLine):
                        # print(lineNum)
                        theadObj = threading.Thread(target=readFile, args=[urls, lineNum, dictFileName, blackResLen, lastTenResLen])
                        theadObjThreads.append(theadObj)
                        theadObj.start()
                    for theadObj in theadObjThreads:    # 等待所有这一轮的线程结束
                        theadObj.join()
                    print('\n一组线程结束')
                    # time.sleep(33)
                else:
                    urlsLines += int(threadNum)
                    readedUrlLine += urlsLines
                    # print(readedUrlLine)
                    for lineNum in range(readedUrlLine - urlsLines, readedUrlLine):
                        # print(11111111)
                        # print(lineNum)
                        theadObj = threading.Thread(target=readFile, args=[urls, lineNum, dictFileName, blackResLen, lastTenResLen])
                        theadObj.start()
                        theadObj.join()
                    break
    else:
        usage()

if __name__ == '__main__':
    main()
