#coding:UTF-8
import requests # 处理请求的库
import random   # timgout需要用到随机数，以防止被识别为爬虫
import time # 时间相关操作
import socket   # socket和http.client用于处理异常状态
import http.client
import re   # 正则库
import numpy as np  # numpy迭代器对象 numpy.nditer()提供了一种灵活访问一个或者多个数组元素的方式
import pymysql      # 引入数据库
import json
import os
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
    page_arr = {}
    page_arr = re.split(r'\s+', all_page)
    page_arr.remove('/')
    page_arr = {'page_l': page_arr[0], 'page_r': page_arr[1]}
    page_arr = json.dumps(page_arr)

    # 把拿到的图片url和copyright组合赋值给final[]
    final = {}
    sun = {}
    for i, j, n in zip(img_data, copyright_data, range(len(copyright_data))):
        sun['data'+ str(n)] = {'url': i, 'copyright': j}
    # final = json.dumps(final, ensure_ascii=False)   # dict转json，后面的让它保持原来的编码，防止中文乱码
    # final = np.array(final)
    final['images'] = sun
    final['page_num'] = page_arr

    return final

# 实现提取多维嵌套的json、字典dict、列表list、元组tuple内的数据
def get_target_value(key, dic, tmp_list):
    # :param key: 目标key值
    # :param dic: JSON数据
    # :param tmp_list: 用于存储获取的数据
    # :return: list
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list

    for value in dic.values():  # 传入数据不符合则对其value值进行遍历
        if isinstance(value, dict):
            get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
        elif isinstance(value, (list, tuple)):
            _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value

    return tmp_list

def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):  
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)       # 传入数据的value值是列表或者元组，则调用自身

def Write_data(data,name):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apnh,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0(windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    # w_data = json.dumps(data, ensure_ascii=False)
    file_name_arr = get_target_value('copyright',data, [])
    file_url = get_target_value('url', data, [])
    file_name = []
    for name in file_name_arr:
        # 只取第一个逗号前的字符，去掉全角，】,转化返回值为str以便后续连接文件名所需的字符
        chinese_name = re.search(r'\w+[^，】\s+]', name).group(0)
        t = chinese_name + '.jpg'
        file_name.append(t)
    path = os.path.abspath(os.path.dirname(__file__)) + "\\images\\"
    for i, j in zip(file_url, file_name):
        d_img = requests.get(i, headers = header)
        # with open(os.path.join(path, j), 'wb') as f:
        with open(j, 'wb') as f:
            f.write(d_img.content)

def Conn_sql():
    with open('getBingImgs.csv', 'r', encoding='utf-8') as f:
        datas = f.readlines()
        for i in datas:
            for j in i:
                # t = json.loads(j)
                print('i:',i, end='\n')
                print('j:',j,end='\n')
    # img_url.append(data[0][:,0])
    # img_copyright.append(data[0][:,1])
    # print('url集:',img_url)
    # print('copyr集:', img_copyright)
    # conn = pymysql.connect(
    #     host = 'localhost',
    #     port = 3306,
    #     user = 'root',
    #     password = 'root',
    #     db = 'pythonbing_db'
    # )
    # try:
    #     with conn.cursor() as cursor:
    #         # sql = 'insert into bingimgs_table(url, copyright) values (%s,%s)'
    #         for k,v in data:
    #             t = json.loads(v[k])
    #             print(t, end='\n')
    #             # sql = 'insert into bingimgs_table(url, copyright) values (%s,%s), (t["url"],t["copyright"])'
    #             # cursor.execute(sql)
    #             # conn.commit()
    # except Exception as e:
    #     print(str(e))

if __name__ == '__main__':
    url = 'https://bing.ioliu.cn/?p='
    html = Get_content(url)
    result = Get_data(html)
    # print(type(result),result)
    Write_data(result, 'bing_imgs.txt')
    # Conn_sql()