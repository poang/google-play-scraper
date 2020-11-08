# google-play-scraper
# 爬取Google Play物联网app  
基于requests的爬虫程序，用于爬取google play上的物联网app信息，使用三方网站进行下载  

三方网站：[ https://apkpremier.com/]( https://apkpremier.com/)

使用方法： 

- 首先运行get\_app\_info.py文件，获取物联网app信息，将以下信息保存进csv文件中：
  - app\_id
  - app名称
  - app描述
  - 当前页面url
  - 隐私协议网址
- 然后运行download.py，利用selenium虚拟点击，在第三方网站进行。
