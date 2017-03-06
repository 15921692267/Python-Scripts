#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : lizhenliang

import sys, re

def log_analyze(log_file, start_time=None, end_time=None):
    total_count = {}
    ip_count = {}
    ip_time_count = {}
    status_code_count = {}
    request_url_count = {}
    error_status_code = {'4xx':{},'5xx':{}}
    with open(log_file) as file:
        for line in file:          # 系统将文件作为生成器对象处理，可处理大文件
            if not line: break
            m = re.search(r'(.*?) (.*?) (\[.*?\]) (\".*?\") (\d+) (\d+) (\".*?\") (\".*?\") (\".*?\")', line)
            ip = m.group(1)
            date_time = m.group(3)[1:-7]
            request_url = m.group(4)[5:-10]
            status_code = m.group(5)
            body_size = m.group(6)
            referer = m.group(7)[1:-1]
            user_agent = m.group(8)[1:-1]

            if start_time and end_time:
                if date_time >= start_time and date_time <= end_time:
                    # 第一次处理会报key错误。下次如果有相同的key，则覆盖现有的key，并次数+1
                    if status_code.startswith('4'):
                        try:
                            counter = error_status_code['4xx'][request_url][1] + 1
                            error_status_code['4xx'][request_url] = [status_code, counter]
                        except KeyError:
                            error_status_code['4xx'][request_url] = [status_code, 1]
                    elif status_code.startswith('5'):
                        try:
                            counter = error_status_code['5xx'][request_url][1] + 1
                            error_status_code['5xx'][request_url] = [status_code, counter]
                        except KeyError:
                            error_status_code['5xx'][request_url] = [status_code, 1]

                    ip_count[ip] = ip_count.get(ip, 0) + 1
                    ip_time_count['%s %s' % (ip, date_time)] = ip_time_count.get('%s %s' % (ip, date_time), 0) + 1
                    request_url_count[request_url] = request_url_count.get(request_url, 0) + 1
                    status_code_count[status_code] = status_code_count.get(status_code, 0) + 1
            else:
                if status_code.startswith('4'):
                    try:
                        counter = error_status_code['4xx'][request_url][1] + 1
                        error_status_code['4xx'][request_url] = [status_code, counter]
                    except KeyError:
                        error_status_code['4xx'][request_url] = [status_code, 1]
                elif status_code.startswith('5'):
                    try:
                        counter = error_status_code['5xx'][request_url][1] + 1
                        error_status_code['5xx'][request_url] = [status_code, counter]
                    except KeyError:
                        error_status_code['5xx'][request_url] = [status_code, 1]

                ip_count[ip] = ip_count.get(ip, 0) + 1
                ip_time_count['%s %s' % (ip, date_time)] = ip_time_count.get('%s %s' % (ip, date_time), 0) + 1
                request_url_count[request_url] = request_url_count.get(request_url, 0) + 1
                status_code_count[status_code] = status_code_count.get(status_code, 0) + 1

    ip_count = sorted(ip_count.iteritems(),key=lambda c:c[1], reverse=True)
    ip_time_count = sorted(ip_time_count.iteritems(),key=lambda c:c[1], reverse=True)
    request_url_count = sorted(request_url_count.iteritems(),key=lambda c:c[1], reverse=True)
    status_code_count = sorted(status_code_count.iteritems(),key=lambda c:c[1], reverse=True)

    total_count['ip'] = ip_count
    total_count['ip_time_count'] = ip_time_count
    total_count['status_code'] = status_code_count
    total_count['request_url'] = request_url_count
    total_count['error_status_code'] = error_status_code
    
    return total_count

if __name__ == '__main__':
    argv_length = len(sys.argv)-1
    if argv_length == 3:
        log_file = sys.argv[1]
        start_time = sys.argv[2]
        end_time = sys.argv[3]
        result = log_analyze(log_file, start_time, end_time)
    elif argv_length == 1:
        log_file = sys.argv[1]
        result = log_analyze(log_file)
    else:
        script_name = sys.argv[0]
        print("Usage1: %s log_file" % script_name) 
        print("Usage2: %s log_file <start_time> <end_time>" % script_name) 
        sys.exit()
    ip_top10 = result['ip'][0:10]
    request_url_top10 = result['request_url'][0:10]
    ip_time_top10 = result['ip_time_count'][0:10]
    status_code_statistics = result['status_code']
    status_code_4xx = result['error_status_code']['4xx']
    status_code_4xx = sorted(status_code_4xx.iteritems(),key=lambda c:c[1][1], reverse=True)[0:10]
    status_code_5xx = result['error_status_code']['5xx'] 
    status_code_5xx = sorted(status_code_5xx.iteritems(),key=lambda c:c[1][1], reverse=True)[0:10]
    print("访问最高的10个IP:")
    for i in ip_top10:
        print(i)
    print("##############################################")    
    print("每秒访问最高的10个IP:")
    for i in ip_time_top10:
        print(i)
    print("##############################################")      
    print("请求最高的10个页面:")
    for i in request_url_top10:
        print(i)
    print("##############################################")      
    print("HTTP状态码统计:")
    for i in status_code_statistics:
        print(i)
    print("##############################################")      
    print("请求状态码4xx的最高10个页面:")
    for i in status_code_4xx:
        print(i)
    print("##############################################")      
    print("请求状态码5xx的最高10个页面:")
    for i in status_code_5xx:
        print(i)
