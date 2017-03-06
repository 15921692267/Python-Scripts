#!/usr/bin/env python
# coding: utf-8

__author__ = 'lizhenliang'

import urllib2 
import string
import smtplib
import time

date_time = time.strftime('%Y-%m-%d %H:%M:%S')

urls = {
    '百度':'www.baidu.com',
    '腾讯':'www.qq.com',
    '新浪':'www.sina.com.cn',
    '阿里':'www.aliyun.com',
    '新网':'www.xinnet.com',
    '万网':'www.neta.cn',
    '京东':'www.jd.com',
    '美团':'www.meituan.com'
}

def sendMail(body):   
    smtp_server = 'smtp.163.com'
    from_mail = 'baojingtongzhi@163.com'
    mail_pass = 'xxx'
    to_mail = ['xxx@163.com', 'xxx@qq.com']
    from_name = u"管理员".encode('gbk')
    subject = u"网站异常".encode('gbk')
    
    to_mail_string = ','.join(to_mail)
    msg = string.join((       
            "From: %s <%s>" % (from_name, from_mail),
            "To: %s" % to_mail_string,
            "Subject: %s: %s" % (subject, name),
            "",
            body
            ), "\r\n")
    try:
        server = smtplib.SMTP()      
        server.connect(smtp_server, "25")         
        server.login(from_mail, mail_pass)       
        server.sendmail(from_mail, to_mail, msg)        
        server.quit()  
    except smtplib.SMTPException as e:
        print("Error %s" %e)

# 三次访问不通认为失效
def judge(url):
    counter = 0
    while counter != 3:
    	# 网址无法访问会抛出异常
        try:
            request = urllib2.urlopen(url, timeout=5)
            http_code = request.getcode()
            if http_code == 200:
                return True
            else:
                counter += 1
                time.sleep(3)
        except:
            counter += 1
            time.sleep(3)
    if counter == 3: return False

if __name__ == '__main__':
    for name, url in urls.items():
        name = name.decode('utf-8').encode('gbk')
        if judge(url):
            # print("Date: %s, Name: %s, URL: %s, 模拟访问成功." % (date_time, name, url))
            pass 
        else:
            info = u"模拟访问失败,请检查Tomcat！".encode('gbk')
            sendMail("Date: %s, Name: %s, URL: %s, %s" % (date_time, name, url, info))
            # print("Date: %s, Name: %s, URL: %s, 模拟访问失败,请检查Tomcat!" % (date_time, name, url))
