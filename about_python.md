## <center>python 的一些用法及曾经踩到的坑

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
#### 3.numpy中linspace() 和 arange()
在绘图或者计算函数值的时候，常常需要生成一些序列，比如生成 0~1000 之间的整数。这时，经常用到 Numpy 中的 linspace() 和 arange() ,但 `两者之间区别，在它们的最后一个参数上`。
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
        print(t)    # [ 0.          1.11111111  2.22222222  3.33333333  4.44444444  5.55555556
  6.66666667  7.77777778  8.88888889 10.        ]
        print('\n')

```


#### 4.常用的numpy函数遍历2个数组
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

#### 5.正则需要用到 `re库`
```
    imoprt re

    // 查找class = 'page' 的 div 再从中找 <span>的文本内容
    all_page = res_body.find('div', {'class': 'page'}).find('span').text
    // 匹配多个空格
    page_num = re.split(r'\s+', all_page)

```

#### 6.python中的print()
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