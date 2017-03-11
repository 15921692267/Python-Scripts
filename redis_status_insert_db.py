#!/usr/bin/env python
#coding:utf-8
# Description: 每隔五分钟检查redis状态，并插入数据库，web前端展示
import redis
import MySQLdb
import string
import time
import smtplib
import ConfigParser
import os,sys

def sendMail(text):
    host = "smtp.xxx.com"        #定义smtp主机
    subject = "redisMonitor"      #定义邮件主题
    to_mail = "xxx@163.com"      #邮件收件人
    from_email = "monitor@xxx.com"     #邮件发件人
    password = "xxx"          #邮件发件人邮箱密码
    body = string.join((        #组装sendmail方法的邮件主题内容，各段以"\r\n"进行分割
            "From: %s" % from_email,
            "To: %s" % to_mail,
            "Subject: %s" % subject,
            "",
            text
            ), "\r\n")
    server = smtplib.SMTP()      #创建一个SMTP()对象
    server.connect(host, "25")    #通过connect方法连接smtp主机
    server.starttls()          #启动安全传输模式
    server.login(from_email,password)       #邮箱账户登录认证
    server.sendmail(from_email,to_mail,body)        #邮件发送
    server.quit()       #断开smtp连接

config_file = "redis_info.ini"
if not os.path.exists(config_file):
    print "%s file not exists!" %config_file
    sys.exit()

conf = ConfigParser.ConfigParser()
conf.read(config_file)
redis_num = len(conf.sections())

while True:
    for num in range(redis_num):
        #里面再次读取文件是为了在循环中重新读取
        conf = ConfigParser.ConfigParser()
        conf.read(config_file)
        region = conf.sections()[num]  #获取第一部分标识
        key_list = conf.options(region) #通过第一部分标识获取key
        ip = conf.get(region,key_list[0]) #通过第一部分标识+key获取value
        port = int(conf.get(region,key_list[1]))
        queue_list = conf.get(region,key_list[2]).split(",")  #将queue的值转换为列表
        if conf.get(region,key_list[3]):
            comments = conf.get(region,key_list[3])
        else:
            comments = "Not Configured!"

        count = 0
        while True:
            if count < 3:
                try:
                    db_conn = MySQLdb.Connect(host="127.0.0.1", user='root', passwd='123456', db='cmdb', connect_timeout=3, use_unicode=True, charset="utf8")
                    cursor = db_conn.cursor()
                    table_name = "admin_cmdb_redisservice"
                    count_num = "select count(ip) from %s where ip='%s';" %(table_name, ip)
                    record_num = cursor.execute(count_num)
                    #record_num = int(cursor.fetchall()[0][0])
                    break
                except Exception, e:
                    count +=1
                    continue
            else:
                print "Database connection %s times error: %s" %(count, e)
                sys.exit()

        try:
            pool = redis.ConnectionPool(host=ip, port=port, db=0, socket_timeout=3)
            r = redis.Redis(connection_pool=pool)

            queue_info = []
            for queue_name in queue_list:
                if queue_name:
                    #如果连接失败就跳出执行except语句
                    queue_size = r.llen(queue_name)
                    queue_info.append("%s: %s"%(queue_name,queue_size))
                else:
                    queue_info.append("Not Configured!")
            #再将列表转换成字符串后入库
            queue_size = ', '.join(queue_info)

            #如果获取到版本说明连接正常
            redis_v = "redis " + r.info()['redis_version']
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            status = "OK"
        except Exception, e:
            status = "NO(%s)" %e
            date = time.strftime('%Y-%m-%d %H:%M:%S')
	    #date = datetime.datetime.now()
            try:
                sendMail('%s, %s Redis status is NO! Error: %s' %(date, ip, e))
            except Exception, e:
                print "Send Email error: " +str(e)
		sys.exit()
        finally:
            try:
                # 如果IP已经不存在就插入新记录，否则更新现有状态
                if record_num == 0:
                    if status == "OK":
                        insert_status = "insert into %s(ip,service,port,queue_size,status,update_time,comments) values ('%s','%s','%s','%s','%s','%s','%s');" %(table_name, ip, redis_v, port, queue_size, status, date, comments)
                        print "%s --> %s" %(date, insert_status)
                        cursor.execute(insert_status)
                    else:
                        insert_status = "insert into %s(ip,service,port,queue_size,status,update_time,comments) values ('%s','redis','%s','Null','%s','%s','%s');"   %(table_name, ip, port, status, date, comments)
                        print "%s --> %s" %(date, insert_status)
                        cursor.execute(insert_status)
                elif record_num == 1:
                    if status == "OK":
                        update_status = "update %s set service='%s',port='%s',queue_size='%s',status='%s',update_time='%s',comments='%s' where ip='%s';" %(table_name, redis_v, port, queue_size, status, date, comments, ip)                    
                        print "%s --> %s" %(date, update_status)
                        cursor.execute(update_status)
                    else:
                        update_status = "update %s set service='redis',port='%s',queue_size='Null',status='%s',update_time='%s',comments='%s' where ip='%s';" %(table_name, port, status, date, comments, ip)                    
                        print "%s --> %s" %(date, update_status)
                        cursor.execute(update_status)
                db_conn.commit()
                cursor.close()
                db_conn.close()
            except Exception, e:
                print "Database insert or update error: " +str(e)
    print "sleep 300s..."
    time.sleep(300)

