#coding:UTF-8
import requests # 处理请求的库
import csv  # 保存为csv格式需要用到
import random   # timgout需要用到随机数，以防止被识别为爬虫
import time # 时间相关操作
import socket   # socket和http.client用于处理异常状态
import http.client
import re   # 正则库
import numpy as np  # numpy迭代器对象 numpy.nditer()提供了一种灵活访问一个或者多个数组元素的方式
import pandas as pd # 用pandas函数处理爬取的数据
from bs4 import BeautifulSoup   # 最重要的html解析库,我使用了lxml,比原生的更好解析html

def Get_content(url, data =None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apnh,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0(windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    
    while True:
        try:
            rep = requests.get(url, headers = header, timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as err:
            print('1:', err)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as err:
            print('2:', err)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as err:
            print('3:', err)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as err:
            print('4:', err)
            time.sleep(random.choice(range(5, 15)))
    return rep.text

def Get_data(html_text):
    # 解析TagHtml
    bs = BeautifulSoup(html_text, 'lxml')
    res_body = bs.body
    
    # 取<img>标签内的src文本内容
    all_img = res_body.find_all('img')
    img_data = []
    for the_img in all_img:
        img_data.append(the_img.get('src'))

    # 取<h3>标签之间的文本内容
    all_copyright = res_body.find_all('h3')
    copyright_data = []
    for the_copyright in all_copyright:
        copyright_data.append(the_copyright.text)
    
    # 取得当前页及总页数的数值
    all_page = res_body.find('div', {'class': 'page'}).find('span').text
    # page_num = re.split(r'\s+', all_page)
    page_num = re.split(r'\s+', all_page)
    page_num_arr = np.array(page_num)
    print(page_num_arr)

    # 把拿到的图片url和copyright组合赋值给final[]
    final = []
    sun = {}
    for i, j in zip(img_data, copyright_data):
        sun = {'url': i, 'copyright': j}
        final.append(sun)
    final.append(page_num)
    print(final[-1][0])
    return final

def Write_data(data, name):
    file_name = name
    with open(file_name, 'w', encoding='utf-8') as f:
        # f_csv = csv.writer(f)
        # f_csv.writerows(data)
        pandas_result = pd.DataFrame(f)
        pandas_result.writerows(data)

if __name__ == '__main__':
    url = 'https://bing.ioliu.cn/'
    html = Get_content(url)
    result = Get_data(html)
    # print(result)
    # pandas_result = pd.DataFrame(result)
    # Write_data(result, 'getBingImgs.csv')