# -*- coding: utf-8 -*-


from win10toast import ToastNotifier
from selenium import webdriver
from time import sleep
from datetime import datetime, time, date, timedelta
from lxml import etree
import requests
from bs4 import BeautifulSoup


def getHtmlText():
    header = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'}
    r = requests.get('https://www.smcinema.com/Schedule/PreferenceBranch?movieName=Fate%2FStay%20Night%3A%20Heaven%E2%80%99s%20Feel%20II%20-%20Lost%20Butterfly', headers = header)
    #r = requests.get('https://www.smcinema.com/Schedule/PreferenceBranch?movieName=Backtrace', headers = header)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    branch = soup.find_all('option')
    return branch


def main ():
    toaster = ToastNotifier()
    branchs = getHtmlText()
    while branchs:
        if len(branchs) > 1:
            print('omedeto!')
            driver = webdriver.Chrome()
            driver.get('https://www.smcinema.com/Schedule?mn=Fate%2FStay%20Night%3A%20Heaven%E2%80%99s%20Feel%20II%20-%20Lost%20Butterfly')
            toaster.show_toast('Fate Stay Night')
            break
        else:
            print('Not this time', datetime.now())
            branchs = getHtmlText()
            sleep(60)

if __name__ == '__main__':
    main()