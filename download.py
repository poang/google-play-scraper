import requests
import selenium
import urllib.request
from selenium import webdriver
import time
import re
import pandas as pd
import copy
import os
from queue import Queue
app_lists = []
def loadhtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'cookie': '1P_JAR=2020-10-12-14; NID=204=PNpfJVcHfHDhMa9iVfgdOyqAG1GSvQxoQ70z2Pnj_VnllBQ5QMh0IfYf37ptvprsWpFh2NSlNu1dx7EddgfvZmO4d3YbYMnMdTxg-KVKNeA6f8nD2LxODgw5A2q331mrYCiFN0VgYKmshGBKaouNitsixKlFJa0ceL1ricTF8iQ; OTZ=5670155_24_24__24_'
    }
    respone = requests.get(url=url,headers=headers)
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

    # 获取网页描述
    pattern = re.compile('meta itemprop="description" content="(.*?)">', re.S)
    describation = pattern.findall(page_text)[0]
  #  describation = describation.replace('\n', '')

    # #获取查看更多链接
    # pattern = re.compile('<div class="W9yFB">.*?class="LkLjZd ScJHi U8Ww7d xjAeve nMZKrb  id-track-click ".*?href="(.*?)".*?</a>',re.S)
    # more = pattern.findall(page_text)[0]
    # more = 'https://play.google.com' + more
    # loc = more.find("&")
    # str = more[0:loc+1]
    # str2 = more[loc+5:]
    # url = str + str2
    return name,href,describation
def get_moreurl(ur):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'cookie': '1P_JAR=2020-10-12-14; NID=204=PNpfJVcHfHDhMa9iVfgdOyqAG1GSvQxoQ70z2Pnj_VnllBQ5QMh0IfYf37ptvprsWpFh2NSlNu1dx7EddgfvZmO4d3YbYMnMdTxg-KVKNeA6f8nD2LxODgw5A2q331mrYCiFN0VgYKmshGBKaouNitsixKlFJa0ceL1ricTF8iQ; OTZ=5670155_24_24__24_'
    }
    respone = requests.get(url=ur, headers=headers)
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'cookie': '1P_JAR=2020-10-12-14; NID=204=PNpfJVcHfHDhMa9iVfgdOyqAG1GSvQxoQ70z2Pnj_VnllBQ5QMh0IfYf37ptvprsWpFh2NSlNu1dx7EddgfvZmO4d3YbYMnMdTxg-KVKNeA6f8nD2LxODgw5A2q331mrYCiFN0VgYKmshGBKaouNitsixKlFJa0ceL1ricTF8iQ; OTZ=5670155_24_24__24_'
    }
    app_respone = requests.get(url=url, headers=headers)
    page_text = app_respone.text
    page_info = '<div class="wXUyZd"><a href="(.*?)" aria-hidden="true" tabindex="-1" class="poRVub"></a></div>'
    current_app_lists = re.findall(page_info,page_text,re.S)
    for i in range(len(current_app_lists)):
        current_app_lists[i] = 'https://play.google.com' + current_app_lists[i]
    return current_app_lists

def make_download_url(list):
    apk_list = copy.copy(list)
    for i in range(len(apk_list)):
       # loc = str(list[i]).find("id")
        apk_list[i] ="https://apps.evozi.com/apk-downloader/?id=" + apk_list[i]
    return apk_list

def get_id(apk_url):
    loc = str(apk_url).find("id")
    apk_id =str(apk_url)[loc + 3:]
    return apk_id

def download_apk(url,namelist):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'cookie': '1P_JAR=2020-10-12-14; NID=204=PNpfJVcHfHDhMa9iVfgdOyqAG1GSvQxoQ70z2Pnj_VnllBQ5QMh0IfYf37ptvprsWpFh2NSlNu1dx7EddgfvZmO4d3YbYMnMdTxg-KVKNeA6f8nD2LxODgw5A2q331mrYCiFN0VgYKmshGBKaouNitsixKlFJa0ceL1ricTF8iQ; OTZ=5670155_24_24__24_'
    }
    respone = requests.get(url=url, headers=headers).content
    with open('./apk_down/'+ namelist + '.apk', 'wb') as fp:
        fp.write(respone)

if __name__ == '__main__':
#     url_lists = [] #保存下载url列表
#     app_id = []  #保存的下载apk包名(id)
#     app_name_list = [] #保存app名称
#     describe_list = [] #保存描述
#     privacy_list = [] #保存隐私协议url
#     q = Queue()  # 定义队列
#     url_lists2 = []
#     url = 'https://play.google.com/store/apps/details?id=com.xiaomi.smarthome'
#     url_lists2.append(url)  #将当前页面添加到保存列表中
#     #url_lists.append(url)
#     page = loadhtml(url)
#     id1 = get_id(url)
#    # app_id.append(id1)
#     name,href,describation = Loadpara(page)
#     # app_name_list.append(name)
#     # privacy_list.append(href)
#     # describe_list.append(describation)
#     q.put(url)  # 将url入队列
#     while len(url_lists2)<2300:
#         url1 = q.get()  # 将url出队列
#         more_url = get_moreurl(url1)  # 通过当前url截取查看更多的url
#         list = get_cluster(more_url)  # 通过查看更多url获取更多appurl
#         url_lists2.extend(list)  # 合并list
#         for url4 in url_lists2:
#             if url4 not in url_lists:
#                 url_lists.append(url4)
#         for url in list:
#             q.put(url)
# #    apk_url_list = get_cluster(url1)  #获取米家更多相关的url列表
#     for url2 in url_lists:
#         page = loadhtml(url2)
#         name, href, describation = Loadpara(page)
#         apk_id = get_id(url2)
#         app_id.append(apk_id)
#         app_name_list.append(name)
#         #url_lists.append(url2)
#         privacy_list.append(href)
#         describe_list.append(describation)
#         print(name)


    #     print("正在访问")
    # dataframe = pd.DataFrame({'Apk_Id':app_id,'App_Name':app_name_list,'Url':url_lists,'describation':describe_list,'Privacy Policy':privacy_list})
    # dataframe.to_csv("C:\\Users\\poang\\PycharmProjects\\爬虫学习\\data.csv",index=False)  #C:\\Users\\poang\\PycharmProjects\\爬虫学习\\data.csv
    #
    driver = webdriver.Chrome(executable_path=r"C:\Users\poang\Documents\Tencent Files\517434308\FileRecv\chromedriver.exe")
    path = 'C:\\Users\\poang\\PycharmProjects\\爬虫学习\\iot_apk2.csv'
    df = pd.read_csv(path,encoding='unicode_escape')
    down = df.values.tolist()
    down_lists_id = []
    for down_list in down:
        down_lists_id.append(down_list[2])
   # print(down_lists_id)

    for j in range(200,len(down_lists_id)):
        driver.get('https://apkpremier.com/')
        time.sleep(3)
        url_input = driver.find_element_by_id('search_info')
        time.sleep(3)
        url_input.send_keys(down_lists_id[j])
        time.sleep(3)
        but1 = driver.find_element_by_class_name("search-btn")
        but1.click()
        time.sleep(7)
        print("正在下载！")
   # print(down_lists_id)

   # print(apk_list)
   #  for i in range(21,len(apk_list)+1):  #len(apk_list)+1
   #      driver.get(apk_list[i])
   #      time.sleep(5)
   #      but1 = driver.find_element_by_class_name('btn.btn-lg.btn-block.btn-info.mt-4.mb-4')
   #      but1.click()
   #      time.sleep(7)
   #      ref = driver.find_element_by_xpath('//a[@class="btn btn-success btn-block mt-4 mb-4"]').get_attribute('href')
   #      print(ref)
   #      if '.apk' in ref:
   #          download_apk(ref,down_lists_id[i])
   #
   #      else:
   #          continue
   #
   #      print("正在下载")
   #      if i%10 == 0:
   #          time.sleep(650)
   #  print("下载完成")


