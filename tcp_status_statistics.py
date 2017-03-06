#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

tcp_status = {
    '00':'ERROR_STATUS',
    '01':'ESTABLISHED',
    '02':'SYN_SENT',
    '03':'SYN_RECV',
    '04':'FIN_WAIT1',
    '05':'FIN_WAIT2',
    '06':'TIME_WAIT',
    '07':'CLOSE',
    '08':'CLOSE_WAIT',
    '09':'LAST_ACK',
    '0A':'LISTEN',
    '0B':'CLOSING'
}

def tcp_status_statistics(status):
    tcp_status_count = {
        'ERROR_STATUS':0,
        'ESTABLISHED':0,
        'SYN_SENT':0,
        'SYN_RECV':0,
        'FIN_WAIT1':0,
        'FIN_WAIT2':0,
        'TIME_WAIT':0,
        'CLOSE':0,
        'CLOSE_WAIT':0,
        'LAST_ACK':0,
        'LISTEN':0,
        'CLOSING':0
    }
    with open('/proc/net/tcp') as file:
        while file:
            line = file.readline()
            if not line: break
            status_line = line.split()[3]
            if status_line == "st": continue
            status_name = tcp_status[status_line]
            tcp_status_count[status_name] = tcp_status_count.get(status_name, 0) + 1
        return tcp_status_count[status]

if __name__ == '__main__':
    status = sys.argv[1]
    print tcp_status_statistics(status)

# import sys,os
# def tcp_status_statistics(status):
#     tcp_status_count = os.popen("netstat -antp |awk '{a[$6]++}END{for(i in a)if(i==toupper(\"%s\"))print a[i]}'" % status).read()
#     if not tcp_status_count.strip():
#        return "0"
#     else:
#        return tcp_status_count

# print tcp_status_statistics(sys.argv[1]).strip()
