import requests
import selenium
import urllib.request
from selenium import webdriver
import time
import re
import pandas as pd
import copy
from queue import Queue
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False  # 关闭多余连接
keyword_list = ['smart home','remote','sensor','Wi-Fi','WiFi','IOT','wearable','Bluetooth','robot',
                'health','watchface','fitness']
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
         'cookie': '1P_JAR=2020-10-12-14; NID=204=PNpfJVcHfHDhMa9iVfgdOyqAG1GSvQxoQ70z2Pnj_VnllBQ5QMh0IfYf37ptvprsWpFh2NSlNu1dx7EddgfvZmO4d3YbYMnMdTxg-KVKNeA6f8nD2LxODgw5A2q331mrYCiFN0VgYKmshGBKaouNitsixKlFJa0ceL1ricTF8iQ; OTZ=5670155_24_24__24_'

 }
def loadhtml(url):
    respone = requests.get(url=url,headers=headers,timeout=10)
    return respone.text

def Loadpara(page_text):
    #获取app名称
    pattern = re.compile('<h1\sclass="AHFaub"\sitemprop="name"><span >(.*?)</span>',re.S)
    name = pattern.findall(page_text)[0]
    #获取隐私政策网址
    pattern = re.compile('<div>.*?class="hrTbp euBY6b".*?</div><div><a href="(.*?)" class="hrTbp ">.*?</a></div>',re.S)
    href = pattern.findall(page_text)
    if href:
        href = href[0]
  #  describation = describation.replace('\n', '')
    return name,href
#获取app的类型
def get_category(page_text):
    pattern = re.compile('<a itemprop="genre" href="/store/apps/category/(.*?)".*?>', re.S)
    category = pattern.findall(page_text)
    if category:
        category = category[0]
    return category
#获取app的具体描述
def get_describation(page_text):

    # 获取网页描述
    pattern = re.compile('meta itemprop="description" content="(.*?)">', re.S)
    describation = pattern.findall(page_text)[0]
    return str(describation).lower()

def get_moreurl(ur):
    respone = requests.get(url=ur, headers=headers, timeout=10)
    page_text = respone.text
    pattern = re.compile('<div class="W9yFB">.*?class="LkLjZd ScJHi U8Ww7d xjAeve nMZKrb  id-track-click ".*?href="(.*?)".*?</a>',re.S)
    more = pattern.findall(page_text)
    more = 'https://play.google.com' + more[0]
    loc = more.find("&")
    str = more[0:loc+1]
    str2 = more[loc+5:]
    url = str + str2
    return url

def get_cluster(url):
    app_respone = requests.get(url=url, headers=headers,timeout=10)
    page_text = app_respone.text
    page_info = '<div class="wXUyZd"><a href="(.*?)" aria-hidden="true" tabindex="-1" class="poRVub"></a></div>'
    current_app_lists = re.findall(page_info,page_text,re.S)
    for i in range(len(current_app_lists)):
        current_app_lists[i] = 'https://play.google.com' + current_app_lists[i]
    return current_app_lists

def make_download_url(list):
    apk_list = copy.copy(list)
    for i in range(len(apk_list)):
        loc = str(list[i]).find("id")
        apk_list[i] ="https://apps.evozi.com/apk-downloader/?id=" + str(apk_list[i])[loc+3:]
    return apk_list

def get_id(apk_url):
    loc = str(apk_url).find("id")
    apk_id =str(apk_url)[loc + 3:]
    return apk_id


if __name__ == '__main__':
    url_lists = [] #保存下载url列表
    app_id = []  #保存的下载apk包名(id)
    app_name_list = [] #保存app名称
    describe_list = [] #保存描述
    privacy_list = [] #保存隐私协议url
    q = Queue()  # 定义队列
    url_lists2 = []
    url = 'https://play.google.com/store/apps/details?id=com.xiaomi.smarthome'
    url_lists2.append(url)  #将当前页面添加到保存列表中
    page = loadhtml(url)
    id1 = get_id(url)
    name,href = Loadpara(page)
    # app_name_list.append(name)
    # privacy_list.append(href)
    # describe_list.append(describation)
    q.put(url)  # 将url入队列
    while len(url_lists)<1000:
        url1 = q.get()  # 将url出队列
        more_url = get_moreurl(url1)  # 通过当前url截取查看更多的url
        iot_lists = get_cluster(more_url)  # 通过查看更多url获取更多appurl
        #print(iot_lists)
        # 判断描述信息是否含有IoT类关键词
        for iot_list in iot_lists:
            page = loadhtml(iot_list)
            category = get_category(page)
            if (category == "WEATHER") or (category == "SOCIAL"):
                continue
            else:
                describation = get_describation(page)
                for keyword in keyword_list:
                    if keyword.lower() in describation:
                        url_lists2.append(iot_list)
                        #print(iot_list)
                        break

        for url4 in url_lists2:
            if url4 not in url_lists:
                url_lists.append(url4)
                print(url4)
        for url in url_lists:
            q.put(url)

    for url2 in url_lists:
        page = loadhtml(url2)
        name, href = Loadpara(page)
        describation = get_describation(page)
        apk_id = get_id(url2)

        app_id.append(apk_id)
        app_name_list.append(name)
        privacy_list.append(href)
        describe_list.append(describation)
        print(name)

    dataframe = pd.DataFrame({'Apk_Id':app_id,'App_Name':app_name_list,'Url':url_lists,'describation':describe_list,'Privacy Policy':privacy_list})
    dataframe.to_csv("C:\\Users\\poang\\PycharmProjects\\爬虫学习\\iot_apk.csv",index=False)  #C:\\Users\\poang\\PycharmProjects\\爬虫学习\\data.csv
    # driver = webdriver.Chrome(executable_path=r"C:\Users\poang\Documents\Tencent Files\517434308\FileRecv\chromedriver.exe")


