## <center>js的一些用法理解及踩过的坑

#### 1.数组

###### ①数组索引
```
    // 常用索引及矩阵索引
        var arr = [
            ['a', 'A'],
            ['b', 'B'],
            ['c', 'C']
        ];
        console.log(arr[0][1]);     // A
        console.log(arr[0, 1]);     // ['b', 'B']
        console.log(arr[1][1]);     // B
        console.log(arr[0, 1][1]);   // B

```

###### ②constructor
返回对创建此对象的数组函数的引用
```
        obj.constructor
```
```
    // 简单使用
        var test = new Date();
        if (test.constructor == Array) {
            console.log('this is an Array');
        }  else if (test.constructor == Boolean) {
            console.log('this is a Boolean');
        } else if (test.constructor == Date) {
            console.log('this is a Date');
        } else if (test.constructor == String) {
            console.log('this is a String');
        }

    // 对象式使用
        function test (name, job, born) {
            this.name = name;
            this.job = job;
            this.born = born;
        }
        var bill = new test('bill gates', 'teacher', 1993);
        console.log(bill.job);
```

###### ③prototype
让你可以向对象添加属性和方法
```
        obj.prototype.name = value
```
```
        function test (name, job, born) {
            this.name = name;
            this.job = job;
            this.born = born;
        }
        var bill = new test('bill', 'teacher', 1993);
        test.prototype.salary = null;
        bill.salary = '5K';

        console.log(bill.salary);

```

###### ④concat()
连接两个或更多的数组，并返回结果
```
    /**
     * 参数，必须，可以是具体的值，也可是数组对象，可以任意多个
     * 返回一个新的数组。该数组是把参数添加到 arrayObject 中生成的。
     * 如果 参数 是数组，添加的是数组中的元素，而不是数组
     */
        arrayObject.concat(array1, array2, ..., array8)
```
```
    // 直接连接数值
        var arr = [1, 3, 5];
        console.log(arr.concat(2, 4, 6));
    // 连接数组
        var arr2 = ['a', 'b', 'c'];
        var arr3 = ['A', 'B', 'C'];
        console.log(arr.concat(arr2));
        console.log(arr.concat(arr2, arr3));
    
```

###### ⑤join()
通过指定的分隔符把数组中的所有元素隔开，`数组转为字符串`
```
    /**
     * 可选，指定要使用的分隔符，默认逗号
     * 返回一个字符串。
     * 该字符串是把 arrayObject 的每个元素转为字符串，再把这些字符串以指定的分隔符连接起来
        arrayObject.join(separator)
```
```
        var arr = ['a', 'b', 'c'];
        console.log(arr.join());
        console.log(arr.join('.'));
```

###### ⑥pop()
删除并返回数组的最后一个元素，`会改变原数组`
```
    /**
     * 返回arrayObject最后一个元素
     * 删除 arrayObject 的最后一个元素，数组长度减 1，并返回删除的元素的值。如果数组已经为空，则 pop() 不改变数组，并返回 undefined 值
     */
        arrayObject.pop()
```
```
        var arr = [1, 2, 3, 4];
        console.log('原数组:' + arr);
        console.log('pop返回值：' + arr.pop());
        console.log('pop操作后的数组：' + arr);
```
###### ⑦push()
向数组末尾添加一个或多个元素，并返回新长度，`会改变原数组`
```
    /**
     * 参数，必须
     * 返回新数组长度
     * push()和 pop()使用数组提供的先进后出栈的功能。
     */
        arrayObject.push(newElement, ..., newElements)
```
```
        var arr = [1, 2, 3];
        console.log(arr.push(4));
        console.log(arr);
```

###### ⑧shift()
删除数组第一个元素，并返回被删除的值，`会改变原数组`
```
    /**
     * 返回数组被删除的第一个值
     * 如果数组为空，则返回undefined
     */
        arrayObject.shift()
```
```
        var arr = [1, 2, 3, 4];
        arr.shift();
        console.log(arr);
```

###### ⑨unshift()
向数组开头添加一个或多个元素，并返回新数组，`会改变原数组`
```
    /**
     * 参数，必须，参数会成为新数组的开头元素
     * 返回新数组
     * 无法在Internet Explorer正确工作
     */
        arrayObject.unshift(newElement1, newElement2, ..., newElement8)
```
```
        var arr = [1, 2, 3, 4];
        arr.unshift(0);
        console.log(arr);
```
###### ⑩reverse()
颠倒数组元素的顺序，`会改变原数组`
```
    // 返回颠倒顺序后的数组
        arrayObject.reverse()
```
```
        var arr = [1, 2, 3, 4];
        arr.reverse();
        console.log(arr);
```

###### ⑩①slice()
从已有的数组中返回指定的元素，`不改变原数组，返回的是子数组`
```
   /**
    * 参数，必须
    * start，必须，指定从何处开始选取，如果是负数，就从数组后面的元素开始算，-1即最后一个，-2即倒数第二个，以此类推
    * end，可选，指定从何处结束选取，不指定则从start开始选取全部元素，如果是负数，则从数组尾部开始算起
    * 返回子数组，不改变原数组
    */
        arrayObject.slice(start, end)
```
```
        var arr = [1, 2, 3, 4, 5, 6];
        console.log(arr.slice(1));      // [2, 3, 4, 5, 6]
        console.log(arr.slice(-1));     // [6]
        console.log(arr.slice(1, 3));       // [2, 3]
        console.log(arr.slice(1, -2));      // 坑点，end-2取到倒数第二位前的元素，[2, 3, 4]
        console.log(arr);       //  [1, 2, 3, 4, 5, 6]
```

###### ⑩②splice()
指定元素下标进行元素添加/删除，返回被删除的元素，`会改变原数组`
```
    /**
     * index，必需，要操作的下标
     * howmany，必需，要删除的数量，设置为0，则不删除元素
     * item1，...，itemX，可选，要添加的新元素
     * 返回包含被删元素的新数组，如果有的话
     */
       arrayObject.splice(index, howmany, item1,.....,itemX) 
```
```
        var arr = [1, 2, 3, 4, 5, 6];
        arr.splice(1, 0, 'a');
        console.log(arr);       // [1, "a", 2, 3, 4, 5, 6]
        arr.splice(1, 1, '贰');     // [1, "贰", 2, 3, 4, 5, 6]
        console.log(arr);
```

###### ⑩③sort()
对数组元素排序，`会改变原数组`
```
    /**
     * 参数，可选，必须是函数，指定排序顺序
     * 返回值是对数组的引用，在原数组排序，会改变原数组
     * 如果不给参数，将按照字符编码的顺序进行排序。要实现这一点，应把数组的元素都转换成字符串（如有必要），以便进行比较
     */
        arrayObject.sort(sortby)
```
```
        var arr_str = ['Tom', 'AnDi', 'John', 'Thomas'];
        var arr = [1, 3, 2, 4, 8, 6];
        arr_str.sort();
        arr.sort((a, b) => a - b)
        console.log(arr_str);       // ["AnDi", "John", "Thomas", "Tom"]
        console.log(arr);       // [1, 2, 3, 4, 6, 8]
```

###### ⑩④toString()
把数组转换为字符串，并返回结果
```
        arrayObject.toString()
```
```
        var arr = ['John', 'Tom', 'Amds'];
        console.log(arr.toString());
        console.log(arr);
```

#### 2.for()
```
        var arr = ['a', 'b', 'c']
        for (let i = 0, i < arr.length; i++) {
            console.log(i, arr[i])
        }

```

#### 3. for...in, for...of, forEach()
```

```