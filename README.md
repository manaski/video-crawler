## 开始
出于学习python的目的，想找个事情激发自己的兴趣，所以周末花了两天做了一些事情。

## m3u8 文件下载
1. 找到m3u8文件的请求链接
2. 获得m3u8文件，解析key地址，以及ts视频地址列表
3. 获取解密key，下载ts文件时使用key进行解密
4. 调用ffmpeg对视频列表进行合并

https://blog.csdn.net/weixin_43667990/article/details/89599787

##     流式下载
请求比较大的视频文件可以通过指定range来下载部分内容

https://www.jianshu.com/p/331aa20937ba

## TODO
代码通用化
支持多线程

## 问题记录

### 安装ffmpeg失败
```html
Connection failed [IP: 91.189.88.152 80]
```
执行以下更新仍失败
```html
sudo apt-get update
```
修改apt-get源为国内源
```html
cp /etc/apt/sources.list /etc/apt/sources.list.bak
```
修改内容为国内源
```html
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse

```

https://www.jianshu.com/p/f71814e520ea
