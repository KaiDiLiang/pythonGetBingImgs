<h2><center>python 的一些用法及曾经踩到的坑</center>

[toc]
---
#### 1.python中数组和list
```
    # sklearn测试

    iris = datasets.load_iris()     # 引入指定测试数据类型
    x = iris['data'][:, (2, 3)]     # petal leng, petal width
    y = (iris['target'] == 2).astype(np.int)    # astype()变量类型转换
    print(x)

    # output: [[1.4 0.2]
              [1.4 0.2]
              [1.3 0.2]
              [1.5 0.2]
              ...
              [5.1 1.8]]

```              
x是一个`数组`，数组的元素是一个`二元组`。x[: , :]`左边':'指行范围，右边':'指列范围，冒号则代表全部`，否则就像代码的第四行，指定一个范围。<br>

`无论是':'还是指定范围的(2, 3)，本质都是会被翻译为一个true/false的一维一元数组，每个元素都是代表数组对应位置的元素是否要出现`。<br>

x[y==0, 0]，y==0在print之后其实是[true true false ...],那么x[y==0, 0],就x的前3个元素而言，分别代表返回（包含），返回（包含），不返回（不包含）；而iris['data'][:, (2, 3)],左边的':'代表的行是[true, true, ..., true],全是true。<br>
    
x[y==0, 0], 第二个0是什么呢？y==1解决了行中哪些返回（那些为true的返回），右边的那个数字指返回哪一列，0指返回第一列，就是output中的1.4, 1.4, 1.3, ..., 5.1； 而iris['data'][:, (2, 3)]，指返回的列是第三列和第四列。<br>

`python` 中行列的处理模式是不一样的，`行的取舍是通过true/false数组来实现的，列的取舍通过指定了哪一列`,以矩阵的角度能更好理解。

```
    data = np.array([
        ['http://h1.ioliu.cn/bing/TajRepublic_ZH-CN1657162292_1920x1080.jpg',  
        '泰姬陵 (© Michele Falzone/plainpicture)'
        ],
        ['http://h1.ioliu.cn/bing/Lunarnewyear2020_ZH-CN1554492287_1920x1080.jpg',  
        '【今日春节】 (© bingdian/iStock/Getty Images Plus)'
        ],
        ['http://h1.ioliu.cn/bing/Lunarnewyeareve2020_ZH-CN1514309048_1920x1080.jpg',  
        '【今日除夕】 (© Calvin Chan Wai Meng/Getty Images)'
        ]
    ])
    print('所有行的第0列:', data[:,0])
    print('第一行的所以列:', data[1,:])
```


#### 2.用for...in遍历2个数组
```

    # 坑点，js的for...in总是得到对象的Key或数组，字符串的下标，
    # for...of和forEach()是直接得到值
    # python的for...in有点像js es6的map()

    list1 = ['a', 'b', 'c']
    list2 = [1, 2, 3]
    listSum = []
    for i, j in zip(list1, list2):
        print(i, j)
        t = {'字母':i, '数字':j}
        listSum.append(t)
    print(listSum)

```

#### 3.numpy库array
##### npArray属性:
```
    np_arr.shape[i] : 多维阵列大小（形状）
    np_arr.ndim : 多维阵列的维度
    np_arr.itemsize : 阵列中元素占的空间大小（byte）
    np_arr.nbytes : 阵列元素的大小统计
    np_arr.T : 转置矩阵，只能在维度 <= 2时使用,与self.transpose()效果相同
    np_arr.flat : 阵列扁平化输出

```
##### npArray维度操作：
```
    import numpy as np
    
    np_arr.reshape() : 把数组变更维度
        # 改二维数组，2行4列
        np_arr.reshape(2, 4)
        # 改三维数组
        np_arr.reshape(2, 2, 2)

---------------------------------------

    np.resize() : 重定义矩阵大小
        # 两种使用方式，一种直接对原数组修改，
        # 另一种不会修改原有的数组值

        t_arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
        c_arr = np.resize(t_arr, (3, 3))    # 有返回值，原数组未变
        print('重定义大小后的数组:',c_arr)
        print('原数组未变：', t_arr)

        n_arr = t_arr.resize((3, 3))
        print('重定义后的数组:',c_arr)
        print('原数组被直接修改了:', t_arr)
---------------------------------------
    np.flatten() : 多维阵列收合为一维阵列（扁平化）

```

#### 4.numpy中linspace() 和 arange()
在绘图或者计算函数值的时候，常常需要生成一些序列，比如生成 0~1000 之间的整数。这时，经常用到 Numpy 中的 linspace() 和 arange() , `两者之间区别，在它们的最后一个参数上`。<br>

`arange()生成的序列不包含结束值，linspace()生成的序列包含结束值。`<br>

如果要`使 linspace() 和 arrange() 等效`，可以用 `linspace(初始值, 结束值, 值的个数, endpoint = False)`
```
    # arange()
    # 结束值不包含在序列中
    # 适用于知道序列中相邻两数之间的间隔的情况，比如生成一定范围内奇数或者偶数的序列

        arange(起始值, 结束值, 间隔)

    # linspace()
    # 结束值包含在序列中；
    # 起始指和结束值之间的个数决定了生成何种等分间隔的序列
    # 适合序列长度和序列取值范围已知的情况，比如采样频率为1200 Hz, 也就是说 0~1s 之间有1200 个点
    
        linsapce(起始值, 结束值, 起始指和结束值之间的个数)

```
```
    #生成0~10间的整数序列

        import numpy as py

        # numpy的arange()测试,结束值并不包含在生成的序列中
        x = np.arange(0, 10, 1)
        print('arange()生成的数组:')
        print(x)    # [0 1 2 3 4 5 6 7 8 9]

        # numpy的linspace()测试
        f = np.linspace(0, 10, 10)  # 错误的写法
        y = np.linspace(0, 9, 10)
        y2 = np.linspace(0, 10, 10, endpoint=False)
        print('linspace()生成的数组:')
        print(y)    # [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]
        print(y2)   # [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]
        print('错误参数生成的数组：')
        print(f)    # [ 0.          1.11111111  2.22222222  3.33333333  4.44444444  5.55555556
  6.66666667  7.77777778  8.88888889 10.        ]
        print('\n')

```

#### 5.常用的numpy函数遍历2个数组
numpy迭代器对象 numpy.nditer()提供了一种灵活访问一个或者多个数组元素的方式
```
    import numpy as np
```
###### 基础式迭代
```
    arr = np.arange(6).reshape(2, 3)    # arange()创建一个2*3数组
    print('原数组：')
    print(arr)    # [[0 1 2][3 4 5]]
    print('\n')
    
    print('数组的基本式遍历：')
    for i in np.nditer(arr):
    print(i, end=', ')
    print('\n')

```
###### 控制遍历顺序
```
        # Fortran order,即数组列序优先
    print('改为列序优先的数组：')
    for s in np.nditer(arr, order = 'F'):
        print(s, end=', ')      # 0, 3, 1, 4, 2, 5,
    print('\n')

        # C Order,即数组行序优先
    print('改为行序优先的数组：')
    for l in np.nditer(arr, order = 'C'):
        print(l, end=', ')      # 0, 1, 2, 3, 4, 5,
    print('\n')

```

###### 修改数组中元素的值
```
        # nditer对象有另一个可选参数 op_flags。 
        # 默认 nditer 将视待迭代遍历的数组为只读对象（read-only）
        # 为了在遍历数组的同时，实现对数组元素值得修改，须指定 read-write 或者 write-only 的模式

    print('修改后的数组：')
    for c in np.nditer(arr, op_flags = ['readwrite']):
        c[...] = 2 * c
    print(arr)      # [[ 0  2  4][ 6  8 10]]
    print('\n')

```
###### 外部循环
nditer类的构造器拥有flags参数，它可以接受下列值：

参数    |描述
--------|--------
c_index | 可以跟踪C顺序的索引
f_index | 可以跟踪Fortran顺序的索引
multi-index | 每次迭代可以跟踪一种索引类型
external_loop | 给出的值是具有多个值得一维数组，而不是零维数组

```
    for change in np.nditer(arr, flags = ['external_loop'], order = 'F'):
        print(change, end = ', ')       # [0 6], [2 8], [ 4 10]
    print('\n')

```

###### **广播迭代 (两个数组结合迭代，arr1[val] : arr2[val])**
```
    a = np.arange(0, 60, 5).reshape(3, 4)
    print('第一个数组:')
    print(a, end='\n')
    print('第二个数组:')
    b = np.array([1, 2, 3, 4], dtype = int)
    print(b, end='\n')
    print('修改后的数组为:')
    for x, y in np.nditer([a, b]):
        print('%d:%d' % (x, y), end = ', ')
    print('\n')

```
#### 6.原生数组和reshape()之后的数组
python `原生没有数组这个概念`，`[ ]`在python中称`list` 。二维数组通过`list[i][i]` 进行索引，支持 `:` 范围索引，但是原生只支持一个维度的索引，如 [:4]、[1:]。<br>

`python中使用数组，推荐numpy库内的array`。`numpy` 提供的array可通过 `[x1:x2, y1:y2]模式来索引矩阵`，可通过`array.shape[ ]获取矩阵的行数/列数`，可通过`reshape()进行行列重置`，可通过`.T进行 ‘转置’`。<br>

`matrix` 是numpy的array的一个`子集`，支持 `:` 以及 `shape[i]` 获取行、列数量，但`只支持矩阵形式的二维数组`。
`matrix` 和 `numpy` 的乘法(\*)模式不同，`matrix` 是乘数的行 * 被乘数的列；`array` 是同位数的相乘。<br>

##### **list、array、matrix相互转化：**
```
    list => array: np.array(list)
    list => matrix: np.mat(list)

    array => list: data.toList()
    
    array => matrix: np.asmatrix()
    matrix => array: np.asarray()

    array采用matrix的乘法: np.dot(array1, array2)
    matrix采用同位数的乘法：np.multiply(mat1, mat2)
```
<br>

**shape[ i ]** : `查看数据有多少行多少列`
**reshape()** : `重组数据，重组后的数组和原数组共用一个内存，类似于js的引用概念，不管改变哪个都互相影响`
```
    arr_test = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    arr_test2 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    print('arr_test出来的数据:')
    print(arr_test.shape[0])     # 值是8，因为8个数据
    # print(arr_test.shape[1])     # IndexError: tuple index out of range

    print('arr_test2出来的数据:')
    print(arr_test2.shape[0])      # 值为2，最外层矩阵有2个元素
    print(arr_test2.shape[1])      # 值为4，内层矩阵有4个元素
    # print(arr_test2.shape[2])      # IndexError: tuple index out of range
    
    print('reshape出来的数据:')
    print(arr_test.reshape(2, 4))    # 改为二维数组 [[1 2 3 4]
    [5 6 7 8]]
    print(arr_test.reshape(2, 2, 2))    # 改为三维数组 [ [[1 2][3 4]] [[5 6][7 8]] ]

```

```
    arr = np.linspace(1, 5, 5)
    print(arr)
```
```
    reshape_arr = np.reshape(-1, 1)
    print(reshape_arr)
```



#### 7.正则需要用到 `re库`
```
    imoprt re

    // 查找class = 'page' 的 div 再从中找 <span>的文本内容
    all_page = res_body.find('div', {'class': 'page'}).find('span').text
    // 匹配多个空格
    page_num = re.split(r'\s+', all_page)

```

###### ①匹配某个标点前的所有非特殊字符，即a-z、A-Z、0-9、_、汉字
`坑点：逗号、句号这些区分中、英文字符，即区分全角标点和半角标点`
```
    url = "海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图，加拿大育空 (© Robert Postma/plainpicture)"
    t = re.match(r'\w+[^，]', url)
    print(t)        # 海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图

```

###### ②匹配所有汉字
```
    url = "海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图，加拿大育空 (© Robert Postma/plainpicture)"
    t = re.sub(r'[^\u4e00-\u9fa5]', '', name)
    print(t)        # 海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图加拿大育空

```

###### ③for...in中的group()该搭配re.match()还是re.search()
**深坑**： `re.match()在for...in中用group()`会出现'AttributeError: 'NoneType' object has no attribute 'group''报错。<br>

**原因**：`re.match()只能从头开始匹配，不能从中间开始,for...in中使用它因没有匹配到元素，却调用了group（）方法造了报错`。<br>

**解决方法**：`改用re.search()即可，re.search()是先扫描全部的代码块，再进行提取的。`
```
    file_name_arr = [
        '海恩斯章克申附近克鲁瓦尼国家公园中冰川和山脉的鸟瞰图，加拿大育空 (© Robert Postma/plainpicture)',
        '从国际空间站看纽约市 (© NASA Photo/Alamy)', '泰姬陵 (© Michele Falzone/plainpicture)', 
        '【今日春节】 (© bingdian/iStock/Getty Images Plus)', 
        '【今日除夕】 (© Calvin Chan Wai Meng/Getty Images)', 
        '坦桑尼亚塞伦盖蒂国家公园的斑马和角马 (© Raffi Maghdessian/Cavan Images)',
        '育空怀特霍斯附近的北极光，加拿大 (© Design Pics/Danita Delimont)',
        '凯恩戈姆山脉中的欧亚红松鼠，苏格兰高地 (© Images from BarbAnna/Getty Images)', 
        '阳光照耀下的火山岩山脊，冰岛埃亚菲亚德拉冰盖 (© Erlend Haarberg/Minden Pictures)', 
        '野外探险家亚历克斯·彼得森在胡德山南侧快速滑翔，俄勒冈 (© Richard Hallman/DEEPOL by plainpicture)',
        '白沙国家公园中的石膏沙丘，新墨西哥 (© Grant Kaye/Cavan Images)', 
        '一只勃兰特鸬鹚在洛杉矶海岸石油钻塔下的一群太平洋鲭鱼中觅食，加利福尼亚 (© Alex Mustard/Minden Pictures)'
    ]
    files_name = []
    for name in file_name_arr:
        # 只取第一个逗号前的字符，去掉空格和全角，】,转化返回值为str以便后续连接文件名所需的字符
        chinese_name = re.search(r'\w+[^，】\s+]', name).group(0)
        t = chinese_name + '.jpg'
        files_name.append(t)
    print(files_name)

```

#### 8.python中的print()
```
    print(objects, sep='', end='\n', file=sys.stdout)
    print("{%s,%s}" % (i,j), sep=',')
```
```
    objects: 需要输出的对象，多个对象时用逗号分开
    sep: 设置输出对象间的间隔符号，默认为空格
    end: 设置结尾符号，默认是换行符
    file: 要写入的文件对象，设置该参数时不会输出内容，而是将内容写入指定文件中

```

#### 9.获取当前文件的绝对路径
```
    from pathlib import Path as P
    import os

    base_path = P.cwd()
    base_path2 = os.path.abspath(os.path.dirname(__file__))
```

#### 10.拼接路径
**深坑**：拼接不存在的文件夹时，必须先创建，否则会一直报错
```
    from pathlib import Path as P
```
错误的方法：
```
    name_arr = [
        '第一张图.jpg',
        '第二张图.jpg',
        '第三张图.jpg'
    ]
    for j in name_arr:
        base_path = P.cwd()
        # imgs这个文件夹不存在，所以会一直报with open()这边的错误
        img_path = base_path/'imgs'/j
        with open(img_path, 'wb') as f:
            f.write(res.content)

```
**正确的方法**：
```
    name_arr = [
        '第一张图.jpg',
        '第二张图.jpg',
        '第三张图.jpg'
    ]
    for j in name_arr:
        base_path = P.cwd()
        # imgs这个文件夹不存在，所以得先判断它是否存在，不存在则先创建
        img_path = base_path/'imgs'/j
        with open(img_path, 'wb') as f:
            f.write(res.content)

```

#### 11.从双层结构的json中提取数据
###### 情况1：
&nbsp;&nbsp;&nbsp;结构如：
```
    {
    'images': [{
        'startdate': '20200128',
        "url":"/th?id=OHR.SemucChampey_ZH-CN1774527432_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp",
        "urlbase":"/th?id=OHR.SemucChampey_ZH-CN1774527432","copyright":"Semuc Champey自然公园，危地马拉 (© Joel Sharpe/Getty Images)"
        }]
    }
```
&nbsp;&nbsp;&nbsp;提取数据的方法：
```
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apnh,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0(windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
    }
    json_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    timeout = random.choice(range(3, 9))
    rep = requests.get(json_url, headers=header, timeout=timeout)
    rep.encoding = 'utf-8'
    # 解析json数据
    url_json = json.loads(rep.text)
    img_url = url_json['images'][0]['url']
    print(img_url)

```

###### 情况2：
&nbsp;&nbsp;&nbsp;结构如：
```
    <script type="application/ld+json" id="DATA_INFO">
    {
        "user": {
            "isLogin": true,
            "userInfo": {
                "id": 123456,
                "nickname": "happyJared",
                "intro": "做好寫代碼這事"
            }
        }
    }
    </script>
```

&nbsp;&nbsp;&nbsp;提取数据的方法:
```
        json.loads(bs.find('script', {'type': 'application/ld+json'}).get_text()).get("user").get("userInfo").get("nickname")
```
```
        json.loads(bs.find('script', {'id': 'DATA_INFO'}).get_text()).get("user").get("userInfo").get("nickname")
```