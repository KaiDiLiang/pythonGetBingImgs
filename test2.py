import requests
import re
import time
import random
import os
import json
from pathlib import Path as P
from bs4 import BeautifulSoup


# 测试只取某个符号前字符的正则
# url = "海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图，加拿大育空 (© Robert Postma/plainpicture)"
# t = re.match(r'\w+[^，]', url)
# print(t)

# # 测试for..in中的re.search()返回值拼接字符串
# file_name_arr = [
#     '海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图，加拿大育空 (© Robert Postma/plainpicture)',
#     '从国际空间站看纽约市 (© NASA Photo/Alamy)', '泰姬陵 (© Michele Falzone/plainpicture)', 
#     '【今日春节】 (© bingdian/iStock/Getty Images Plus)', 
#     '【今日除夕】 (© Calvin Chan Wai Meng/Getty Images)', 
#     '坦桑尼亚塞伦盖蒂国家公园的斑马和角马 (© Raffi Maghdessian/Cavan Images)',
#     '育空怀特霍斯附近的北极光，加拿大 (© Design Pics/Danita Delimont)',
#     '凯恩戈姆山脉中的欧亚红松鼠，苏格兰高地 (© Images from BarbAnna/Getty Images)', 
#     '阳光照耀下的火山岩山脊，冰岛埃亚菲亚德拉冰盖 (© Erlend Haarberg/Minden Pictures)', 
#     '野外探险家亚历克斯·彼得森在胡德山南侧快速滑翔，俄勒冈 (© Richard Hallman/DEEPOL by plainpicture)',
#     '白沙国家公园中的石膏沙丘，新墨西哥 (© Grant Kaye/Cavan Images)', 
#     '一只勃兰特鸬鹚在洛杉矶海岸石油钻塔下的一群太平洋鲭鱼中觅食，加利福尼亚 (© Alex Mustard/Minden Pictures)'
# ]
# files_name = []
# for name in file_name_arr:
#     chinese_name = re.search(r'\w+[^，】\s+]', name).group(0)
#     # t = chinese_name.group(0)
#     t = chinese_name + '.jpg'
#     files_name.append(t)
# print(files_name)

# 测试从双层json数据中提取url下载文件并填充以当前日期命名的文件名
def Get_json():
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apnh,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0(windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    url_arr = [
        'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1',
        'http://www.bing.com/HPImageArchive.aspx?format=js&idx=1&n=1',
        'http://www.bing.com/HPImageArchive.aspx?format=js&idx=2&n=1'
    ]
    # 设置超时
    timeout = random.choice(range(3, 9))
    url_list = []
    copyright_list = []
    for i in url_arr:
        rep = requests.get(i, headers=header, timeout=timeout)
        rep.encoding = 'utf-8'
        # 解析json数据
        url_json = json.loads(rep.text)
        url = url_json['images'][0]['url']
        url_list.append('https://cn.bing.com' + url)
        img_copyright = url_json['images'][0]['copyright']
        img_copyright = re.search(r'\w+[^，】\s+]', img_copyright).group(0)
        copyright_list.append(img_copyright + '.jpg')

    return url_list,copyright_list

def Download_file(url_lists):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apnh,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0(windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    timeout = random.choice(range(4, 12))
    base_path = P.cwd()
    # imgs这个文件夹不存在，所以得先判断它是否存在，不存在则先创建
    sel_dir = P.exists(base_path/'imgs')
    if (sel_dir):
        img_path = base_path/'imgs'
        for i,j in zip(url_lists[0], url_lists[1]):
            res = requests.get(i, timeout = timeout, headers=header)
            with open(img_path/j, 'wb') as f:
                f.write(res.content)
    else:
        P.mkdir(base_path/'imgs')
        img_path = base_path/'imgs'
        for i,j in zip(url_lists[0], url_lists[1]):
            res = requests.get(i, timeout = timeout, headers=header)
            with open(img_path/j, 'wb') as f:
                f.write(res.content)
        
    time.sleep(random.choice(range(2, 4)))

url_lists = Get_json()
Download_file(url_lists)

# def Download_imgs():
#     header = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apnh,*/*;q=0.8,application/signed-exchange;v=b3',
#         'Accept-Encoding': 'gzip,deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9',
#         'Connection': 'keep-alive',
#         'User-Agent': 'Mozilla/5.0(windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
#     }
#     name_arr = [
#         '第一张图.jpg',
#         '第二张图.jpg',
#         '第三张图.jpg'
#     ]
#     res_data = [
#         'http://cn.bing.com/th?id=OHR.SemucChampey_ZH-CN1774527432_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp',
#         'http://cn.bing.com/th?id=OHR.AerialKluaneNP_ZH-CN4080112842_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp',
#         'http://cn.bing.com/th?id=OHR.NYCLitUp_ZH-CN1703735322_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp'

#     ]
#     timeout = random.choice(range(3, 9))
#     base_path = P.cwd()
#     # imgs这个文件夹不存在，所以得先判断它是否存在，不存在则先创建
#     sel_dir = P.exists(base_path/'imgs')
#     if (sel_dir):
#         img_path = base_path/'imgs'
#         for i,j in zip(name_arr, res_data):
#             res = requests.get(j, timeout = timeout, headers=header)
#             with open(img_path/i, 'wb') as f:
#                 f.write(res.content)
#     else:
#         P.mkdir(base_path/'imgs')
#         img_path = base_path/'imgs'
#         for i,j in zip(name_arr, res_data):
#             res = requests.get(j, timeout = timeout, headers=header)
#             with open(img_path/i, 'wb') as f:
#                 f.write(res.content)
        
#     time.sleep(random.choice(range(2, 4)))