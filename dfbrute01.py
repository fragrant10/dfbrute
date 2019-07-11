#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
@Author: fragrant
'''
from fake_useragent import UserAgent
import requests, sys, os, time, threading, urllib, pyfiglet, terminal_banner

# 随机ua
def headersRandom():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    return headers

# 读文件 url集合 和字典
def readFile(fileName, lineNum, dictFileName):
    with open(fileName, 'r') as file:
        url = file.readlines()[lineNum].strip()
        print('-- scanning -- {0}'.format(url))
        readDictFileAndBrute(url, dictFileName)
        # return url


# 读
def readDictFileAndBrute(url, dictFileName):
    with open(dictFileName, 'r') as file:
        for line in file:
            urlNew = url + line.strip()
            # print(urlNew)
            try:
                res = requests.get(urlNew, headers=headersRandom(), timeout=50)
                time.sleep(0.5)
                # print(res.request.headers)
                # print(res.status_code)
                if res.history:
                    for is301302403405401 in res.history:
                        if is301302403405401.status_code in [301, 302, 401, 403, 405]:
                            print('[+] %s -> %s (CODE: %s|SIZE:%s)' % (urlNew, urllib.parse.unquote(res.url, encoding='utf-8', errors='replace') ,is301302403405401.status_code, len(res.text)), end="\r")
                # print(res.history)
                # print(res.url)
                elif res.ok:
                    print('[+] %s (CODE: %s|SIZE:%s)' % (urlNew, res.status_code, len(res.text)))
                else:
                    print('[-] %s (CODE: %s|SIZE:%s)' % (urlNew, res.status_code, len(res.text)), end="\r")
                    # print('res.status_code {0}'.format())
            except Exception as error:
                # time.sleep(300)
                print('URL: ' + urlNew + 'length: ' + 'None')
                print('Error: ' , error)

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
            readDictFileAndBrute(url, dictFileName)
        elif os.path.exists(urls):
            urlsLines = len(open(urls,'rU').readlines())    # 域名文件有多少行
            print(urlsLines)
            readedUrlLine = 0   # 已经读取过的url行数
            while True:
                urlsLines -= int(threadNum) # 域名文件还剩多少行 为了防止ip被封 每个线程只分配一个url进行扫描
                if urlsLines >= 0:
                    readedUrlLine += int(threadNum) # 记录读过的行数
                    theadObjThreads = [] # 线程列表
                    for lineNum in range(readedUrlLine-int(threadNum), readedUrlLine):
                        # print(lineNum)
                        theadObj = threading.Thread(target=readFile, args=[urls, lineNum, dictFileName])
                        theadObjThreads.append(theadObj)
                        theadObj.start()
                    for theadObj in theadObjThreads:    # 等待所有这一轮的线程结束
                        theadObj.join()
                    print('\n一组多线程结束')
                    # time.sleep(33)
                else:
                    urlsLines += int(threadNum)
                    readedUrlLine += urlsLines
                    # print(readedUrlLine)
                    for lineNum in range(readedUrlLine - urlsLines, readedUrlLine):
                        # print(11111111)
                        # print(lineNum)
                        theadObj = threading.Thread(target=readFile, args=[urls, lineNum, dictFileName])
                        theadObj.start()
                        theadObj.join()
                    break
    else:
        usage()



if __name__ == '__main__':
    main()
