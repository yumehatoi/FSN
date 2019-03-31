# -*- coding: utf-8 -*-


from win10toast import ToastNotifier
import requests
from bs4 import BeautifulSoup
from random import choice
from apscheduler.schedulers.blocking import BlockingScheduler



def getHtmlText(proxy):
    global branch_list
    header = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'}
    r = requests.get('https://www.smcinema.com/Schedule/PreferenceBranch?movieName=Fate%2FStay%20Night%3A%20Heaven%E2%80%99s%20Feel%20II%20-%20Lost%20Butterfly', headers = header, proxies = proxy)
    #r = requests.get('https://www.smcinema.com/Schedule/PreferenceBranch?movieName=Backtrace', headers = header)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    branch_list = list(branch.text for branch in soup.find_all(value="3" or "59"))#value="3" or "59"
    return branch_list

def getIppool ():
    global IPpool
    IPpool_cache = []
    daili_url = 'https://www.kuaidaili.com/free/intr/'
    header = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1'}
    for page in range(6, 10):
        html = requests.get(daili_url + str(page) + '/', headers = header).text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('tr')
        for tr in table:
            try:
                ip = tr.find_all('td')[0].text.strip()
                port = tr.find_all('td')[1].text.strip()
                IPpool_cache.append('http://' + ip + ':' + port)
            except:
                pass
    IPpool = IPpool_cache
    print(IPpool)
    return IPpool

def Toast():
    toaster = ToastNotifier()
    toaster.show_toast('Fate Stay Night{}'.format(branch_list))
    print(branch_list)

def main_job():
    proxy = {'http':choice(IPpool)}
    getHtmlText(proxy)
    if branch_list:
        print('omedeto!')
        Toast()
    else:
        proxy = {'http':choice(IPpool)}
        getHtmlText(proxy)
        print('Not this time {}\n{}\n{}'.format(datetime.now(), proxy, branch_list))


def main ():
    getIppool()
    scheduler = BlockingScheduler()
    scheduler.add_job(getIppool, 'interval', hours=12)
    scheduler.add_job(main_job, 'interval', seconds=60)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main ()