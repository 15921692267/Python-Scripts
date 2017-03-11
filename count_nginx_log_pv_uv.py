#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
import sys

previous_one_minute = (datetime.today() - timedelta(minutes=1)).strftime('%d/%b/%Y:%H:%M')

def test(log_file):
    count = {}
    ip_access_num = {}
    minute_count = 0
    with open(log_file) as file:
        for line in file:
            if not line: break
            time_line = line.split(' ')[3][1:-3] 
            ip = line.split()[0]
            if time_line == previous_one_minute:
                minute_count += 1  # 统计前一分钟PV
                ip_access_num[ip] = ip_access_num.get(ip, 0) + 1   # 统计前一分钟UV
    count['pv'] = minute_count
    count['uv'] = len(ip_access_num)
    return count

if __name__ == '__main__':
    log_file = sys.argv[1]
    print test(log_file)

