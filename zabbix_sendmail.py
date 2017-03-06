#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import smtplib
import string

to_mail = sys.argv[1]
subject = sys.argv[2]
body = sys.argv[3]

def sendMail(body):   
    smtp_server = 'smtp.163.com'
    from_mail = 'baojingtongzhi@163.com'
    mail_pass = 'xxx'
    # to_mail = ['xxx@163.com', 'xxx@qq.com']
    from_name = 'Zabbix'
    # subject = u"网站异常".encode('gbk')
    
    to_mail_str = to_mail.replace(' ',',')
    to_mail_list = to_mail_str.split(',')

    msg = string.join((       
            "From: %s <%s>" % (from_name, from_mail),
            "To: %s" % to_mail_str,
            "Subject: %s" % (subject.decode('utf-8').encode('gbk')),
            "",
            body
            ), "\r\n")
    try:
        server = smtplib.SMTP()      
        server.connect(smtp_server, "25")         
        server.login(from_mail, mail_pass)       
        server.sendmail(from_mail, to_mail_list, msg)        
        server.quit()  
    except smtplib.SMTPException as e:
        print("Error %s" %e)

sendMail(body)