#CrawJandanSpider

import re
import os
import time
import threading
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup
import random

headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.87 Safari/537.36'}
path = r"D:\mztue"

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_img_url():
    g = ['http://jandan.net/ooxx/page-' + str(num) for num in range(90,120)]
    img_lists = []
    for i in g:
        html = requests.get(i, headers=headers, timeout = 30)
        page = html.text
        soup = BeautifulSoup(page, 'html.parser')
        img_list = soup.find_all('img')
        img_lists.append(img_list)
    return(img_lists)

def get_img_url_lists(img_lists):

    imglist = []

    for i in range(0, img_lists.__len__()):
        img_lists[i] = str(img_lists[i])
        imglist.append(img_lists[i])

    imgstr = ''.join(imglist)

    img_url_list = re.findall(r'src="(.*?.jpg)"', imgstr)

    img_str = 'https:'.join(img_url_list)

    img_url_lists = re.findall(r'(https://.*?.jpg)', img_str)

    return img_url_lists


def save_imgs(img_url_lists):

    try:
        if not os.path.exists(path):
            os.mkdir(path)
            os.chdir(path)
            x = 0
            for i in img_url_lists:
                r = requests.get(i)
                imgname = "{}.jpg".format(x)
                x+=1
                with open(imgname, 'ab') as f:
                    f.write(r.content)
                    print(imgname)
        else:
            print('file exist')
    except:
        print('fail')






if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/'
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    
    
    img_lists = get_img_url()
    img_url_lists = get_img_url_lists(img_lists)
    save_imgs(img_url_lists)

    print(proxies)

    
