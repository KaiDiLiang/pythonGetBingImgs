import numpy as np
from sklearn import datasets    # sklearn模块封装了常用的递归、降维、分类、聚类等方法,并提供一些标准数据

# numpy的测试
arr = np.arange(6).reshape(2, 3)    # arange()创建一个2*3数组
print('原数组：')
print(arr)    # [[0 1 2][3 4 5]]
print('\n')

print('数组的基本式遍历：')
for i in np.nditer(arr):
    print(i, end=', ')
print('\n')

    # 控制遍历顺序

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

    # nditer对象有另一个可选参数 op_flags。 
    # 默认 nditer 将视待迭代遍历的数组为只读对象（read-only）
    # 为了在遍历数组的同时，实现对数组元素值得修改，须指定 read-write 或者 write-only 的模式

print('修改后的数组：')
for c in np.nditer(arr, op_flags = ['readwrite']):
    c[...] = 2 * c
print(arr)
print('\n')

print('遍历并组合为一维数组：')
for change in np.nditer(arr, flags = ['external_loop'], order = 'F'):
    print(change, end = ', ')
print('\n')

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

# numpy的arange()测试
x = np.arange(0, 10, 1)
print('arange()生成的数组:')
print(x)

# numpy的linspace()测试
f = np.linspace(0, 10, 10)
y = np.linspace(0, 9, 10)
y2 = np.linspace(0, 10, 10, endpoint=False)
print('linspace()生成的数组:')
print(y)
print(y2)
print('错误的参数生成的数组:')
print(f)
print('\n')

# for...in zip()测试
list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]
listSum = []
for i, j in zip(list1, list2):
    print(i, j)
    t = {'字母':i, '数字':j}
    listSum.append(t)
print(listSum, end='\n')

# sklearn测试
iris = datasets.load_iris() # 引入指定测试数据类型
x = iris['data'][:, (2, 3)] # petal leng, petal width
y = (iris['target'] == 2).astype(np.int)    # astype()变量类型转换
print(x)



