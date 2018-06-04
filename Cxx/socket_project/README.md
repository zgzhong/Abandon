# Readme 文件
这个文件是project文档中要求的，所以我按照文档的要求进行编写。您需要自己转换成符合文档要求的英文文档

## project结构及各个文件实现的功能
1. **aws.h**
   定义了`Result`类, 该类负责对处理ServerA/B/C传回的数据和负责将这些数据转化为client和monitor的输出数据
2. **aws.cc**:
	aws服务器主程序实现，是aws服务器逻辑的实现代码。
3. **client.cc**
	client主程序实现，负责接收用输入，往服务器发送查询，并输出aws服务器返回的结果
4. **monitor.cc**:
	monitor主程序实现，与服务器建立长连接，并输出服务器查询的结果。
5. **peer.h**
	对TCP和UDP socket操作进行了封装，定义了一系列的socket类，重用代码以便简化主程序
6. **peer.cc**:
	实现了*peer.h*文件中定义的socket类。
7. **global.h**
	该项目的公共类，该头文件中定义了aws, serverA/B/C, client公用的结构。并且定义了一些全局变量如静态结构。
7. **server_util.h**: 
	该头文件定义了serverA/B/C通用的函数。例如读取文件。search, prefix, suffix等操作。
8. **serverA.cc**: 
	serverA主程序
9. **serverB.cc**: 
	serverB主程序
10. **serverC.cc**: serverC主程序

## 实现功能
- search
- prefix
- suffix: (加分的那一项，需要在README中指出)

## 编译
```
$ make all
```

## 启动顺序
aws -> serverA/B/C -> monitor -> client


## 注意事项
1. 程序中没有对client的输入正确性进行检查。如果输入function不是(search、prefix、suffix)中的一个的话，默认是进行search操作。
2. 本程序的所有代码没有重用其他任何project的代码。均为自己实现
3. 本project使用了部分C++11的特性，需要g++ 4.8及以上。



## 另外
文档中要求打包的文件不包含CMakeLists.txt和backendA/B/C.txt这几个文件，你打包的时候需要删除掉。