# -*- coding: utf-8 -*-


from win10toast import ToastNotifier
from selenium import webdriver
from time import sleep
from datetime import datetime, time, date, timedelta
from lxml import etree
import requests
from bs4 import BeautifulSoup
from random import choice


def getHtmlText(proxy, filmname):
    header = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'}
    r = requests.get('https://www.smcinema.com/Schedule/PreferenceBranch?movieName=' + filmname, headers = header, proxies = proxy)
    #r = requests.get('https://www.smcinema.com/Schedule/PreferenceBranch?movieName=Backtrace', headers = header)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    branch = soup.find_all('option')
    return branch

def getIppool (daili_url, daili_page):
    IPpool = []
    header = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'}
    for page in range(1,daili_page):
        html = requests.get(daili_url + str(page) + '/', headers = header).text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('tr')
        for tr in table:
            try:
                ip = tr.find_all('td')[0].text.strip()
                port = tr.find_all('td')[1].text.strip()
                IPpool.append('http://' + ip + ':' + port)
            except:
                pass
    print(IPpool)
    return IPpool

def Toast():
    toaster = ToastNotifier()
    return toaster.show_toast('Fate Stay Night')

def main (daili_url, daili_page, filmname):
    IPpool = getIppool(daili_url, daili_page)
    proxy = {'http':choice(IPpool)}
    branchs = getHtmlText(proxy, filmname)
    while branchs:
        if len(branchs) > 1:
            print('omedeto!')
            while True:
                Toast()
                sleep(5)
        else:
            print('Not this time', datetime.now())
            proxy = {'http':choice(IPpool)}
            branchs = getHtmlText(proxy, filmname)
            print(proxy)
            print(branchs)
            sleep(60)

daili_url = 'https://www.kuaidaili.com/free/intr/'
daili_page = 5
filmname = 'Fate%2FStay%20Night%3A%20Heaven%E2%80%99s%20Feel%20II%20-%20Lost%20Butterfly'

if __name__ == '__main__':
    main (daili_url, daili_page, filmname)