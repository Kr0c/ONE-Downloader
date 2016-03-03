#!/usr/bin/env python
#coding:utf-8
#Filename:oneIsAll.py
__author__ = 'Kr0c'

import urllib2
import time
import re
import os

class Spider:
    def __init__(self):
        #文章篇数
        self.pages = 1
        #新增的文章
        self.addition = 0
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0)'}
        #过滤冗余代码的工具
        self.cleaner = Cleaner()
        self.target = '/Users/Kr0c/Documents/oneisall/'
        #判断文件夹是否存在
        if not os.path.exists(self.target):
            os.makedirs(self.target)
        #判断存档文件是否存在
        if not os.path.exists(self.target + 'record.txt'):
            f = open(self.target + 'record.txt','w')
            f.write(str(self.pages))
            f.close()

    #获取页面代码
    def getPage(self):
        try:
            #定义目标url
            url = 'http://caodan.org/' + self.pages + '-content.html'
            #构建请求的request
            request = urllib2.Request(url,headers = self.headers)
            #urlopen获取页面代码
            response = urllib2.urlopen(request)
            #返回response
            info = response.read().decode('UTF-8')
            return info
        #URLError异常处理
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                if e.reason != 'Not Found':
                    print u'\n[-]连接目标url失败,失败原因：\n',e.reason

    #输出过滤后的文字信息
    def outPut(self):
        #接收处理页面代码
        pageCode = self.getPage()
        #正则表达式构建模式
        if int(self.pages) == 614:
            pattern = re.compile('<title>(.*?) \| ONE.*?' + '"day">(.*?)<.*?>(.*?) \/ (.*?)<.*?' + 'JiaThis Button END.*?<p>.*?\/(.*?)<\/p>' + '(.*?)<!-- 336280',re.S)
        elif int(self.pages) == 820:
            pattern = re.compile('<title>(.*?) \| ONE.*?' + '"day">(.*?)<.*?>(.*?) \/ (.*?)<.*?' + 'JiaThis Button END (.*?)><.*?<\/div>(.*?)<!',re.S)
        elif int(self.pages) >= 1206:
            pattern = re.compile('<title>(.*?) \| ONE.*?' + '"day">(.*?)<.*?>(.*?) \/ (.*?)<.*?' + 'JiaThis Button END.*?<p>(.*?)<\/p>' + '(.*?)<!',re.S)
        else:
            pattern = re.compile('<title>(.*?) \| ONE.*?' + '"day">(.*?)<.*?>(.*?) \/ (.*?)<.*?' + 'JiaThis Button END.*?<p>.*?\/(.*?)<\/p>' + '(.*?)<!',re.S)
        #pattern = re.compile('<title>(.*?) \| ONE.*?' + '"day">(.*?)<.*?>(.*?) \/ (.*?)<.*?' + 'JiaThis Button END.*?<p>.*?\/(.*?)<\/p>' + '(.*?)<!',re.S)
        items = re.findall(pattern,pageCode)
        for item in items:
            print u'\n>>>正在获取第%d篇文章...' % (int(self.pages))
            title = item[0]
            author = item[4]
            #过滤正文中的冗余代码
            article = self.cleaner.clean(item[5])
            date = item[3] + u'年' + item[2] + item[1] + u'日'
            #按月创建文件夹，按标题、作者命名文章
            path_month = self.target + item[3] + u'年' + item[2]
            path_txt = path_month + '/' + title + '_' + author + '.txt'
            if not os.path.exists(path_month):
                print u'[+]创建了名为:"%s"的文件夹' % (path_month)
                os.makedirs(path_month)
            #创建并写入文章
            f = open(path_txt,'w')
            f.write(title.encode('utf-8')+'/'+author.encode('utf-8')+'\n'+date.encode('utf-8')+'\n'+article.encode('utf-8'))
            f.close()
            print u'[+]标题：',title,'/',author,u'\n[+]日期：',date
            print u'[+]已保存至：%s' % (path_txt)

    #主函数
    def run(self):
        try:
            #更新开始时间
            begin = time.time()
            #读入文章数存档
            f = open(self.target + 'record.txt','r')
            self.pages = f.readline()
            f.close()
            print '\n======开始更新文章======'
            #若url可访问，则循环调用获取新文章
            while(1):
                self.outPut()
                self.pages = str(int(self.pages)+1)
                self.addition += 1
        except:
            #写入文章数存档
            f = open(self.target + 'record.txt','w')
            f.write(str(int(self.pages)-1))
            f.close()
            #更新结束时间
            end = time.time()
            print u'\n========更新完成========\n[+]新增 %d篇文章\n[+]耗时 %dmin%.2fs\n' % (self.addition,(end - begin) / 60,(end - begin) % 60)

#过滤冗余代码的工具
class Cleaner:
    #替换引号
    replace_qu = re.compile('&quot;')
    replace_ls = re.compile('&lsquo;')
    replace_rs = re.compile('&rsquo;')
    replace_ld = re.compile('&ldquo;')
    replace_rd = re.compile('&rdquo;')
    #替换空格
    replace_sp = re.compile('&nbsp;')
    #替换破折号
    replace_md = re.compile('&mdash;')
    #替换省略号
    replace_he = re.compile('&hellip;')
    #替换°
    replace_de = re.compile('&deg;')
    #将段落标签替换为\t
    replaceP = re.compile('<p><P>|<P>|<p>')
    #将段落结束标签替换为\n
    replace_P = re.compile('<\/p>|<\/P>')
    #将换行符或双换行符替换为\n
    replace_BR = re.compile('<br><br>|<br>|<BR>|<br \/>')
    #将其余标签剔除
    remove_Tag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')
    def clean(self,x):
        x = re.sub(self.replace_qu,u'"',x)
        x = re.sub(self.replace_ls,u'‘',x)
        x = re.sub(self.replace_rs,u'’',x)
        x = re.sub(self.replace_ld,u'“',x)
        x = re.sub(self.replace_rd,u'”',x)
        x = re.sub(self.replace_sp,' ',x)
        x = re.sub(self.replace_md,u'-',x)
        x = re.sub(self.replace_he,u'…',x)
        x = re.sub(self.replace_de,u'°',x)
        x = re.sub(self.replaceP,"   ",x)
        x = re.sub(self.replace_P,"\n",x)
        x = re.sub(self.replace_BR,"\n",x)
        x = re.sub(self.remove_Tag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x

#开始运行
spider = Spider()
spider.run()
