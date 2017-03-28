#!/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ : lizhenliang

import sys
import urllib
import base64
import hmac
from hashlib import sha1
import time
import uuid
import salt.client

if len(sys.argv)-1 != 3:
    script_name = sys.argv[0]
    print("Usage1: %s {app_slb|wap_slb|pc_slb} <instance_name> <weight>" % script_name)
    # print("Usage2: %s {app_slb|site_slb} <instance_name1,instance_name2> <weight>" % script_name)
    print("Example: %s pc_slb web-api_01 0" % script_name)
    sys.exit(2)

app_slb = {'app_01':'i-xxx', 'app_02':'i-xxx'}
wap_slb = {'wap_01':'i-xxx', 'wap_02':'i-xxx'}
pc_slb = {'pc_01':'i-xxx', 'pc_02':'i-xxx'}

# 判断是否输入SLB ID是否存在
def slbID():
    slb_id = sys.argv[1]
    if slb_id == "app_slb":
        slb_id = 'lb-id1'
    elif slb_id == "wap_slb":
        slb_id = 'lb-id2'
    elif slb_id == "pc_slb":
        slb_id = "lb-id3"
    else:
        print("SLB %s not exist!" % slb_id)
        sys.exit(2)
    return str(slb_id)

# 要执行的操作，是一个数组格式。例如：[{"ServerId":"vm-233","Weight":"0"},{"ServerId":"vm-234","Weight":"0"}]
def actionValueString():
    instance_id = sys.argv[2].split(',')
    weight = sys.argv[3]
    lst = []
    for instance_name in instance_id:
        if slbID() == "lb-id1":
            if app_slb.has_key(instance_name):
                instance_id = app_slb[instance_name]
            else:
                print("The instance %s in SLB app-slb Backend server not exist!" % instance_name)
                sys.exit(2)
        elif slbID() == "lb-id2":
            if wap_slb.has_key(instance_name):
                instance_id = wap_slb[instance_name]
            else:
                print("The instance %s in SLB wap-slb Backend server not exist!" % instance_name)
                sys.exit(2)
        elif slbID() == "lb-id3":
            if pc_slb.has_key(instance_name):
                instance_id = pc_slb[instance_name]
            else:
                print("The instance %s in SLB pc-slb Backend server not exist!" % instance_name)
                sys.exit(2)
        lst.append({'ServerId': '%s' % instance_id, 'Weight': '%s' % weight})
    return str(lst)

class BackendServers():
    def __init__(self):
        self.slb_server_address = 'https://slb.aliyuncs.com'
        self.access_key_id = 'xxx'
        self.access_key_secret = 'xxx'
        self.httpmethod = 'GET'

        self.slb_id = slbID()
        self.action = 'SetBackendServers'
        #self.action = 'DescribeLoadBalancerAttribute'
        self.action_value_string = actionValueString()

    def percentEncode(self, str):
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
        # 特殊字符替换成十六进制表示
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res
    
    # 计算签名
    # 签名计算说明文档：https://help.aliyun.com/document_detail/27572.html?spm=5176.doc27583.6.111.rKsNHA
    def computeSignature(self, parameters, access_key_secret):
        # 对传入的parameters以键进行排序
        sort_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        normalize_query_string = ''
        for (k,v) in sort_parameters:
            # 将排序的字典元素以&Format=JSON形式拼接
            normalize_query_string += '&' + self.percentEncode(k) + '=' + self.percentEncode(v)
        string_to_sign = self.httpmethod + '&%2F&' + self.percentEncode(normalize_query_string[1:])
        # print "string_to_sign:",string_to_sign
        # 计算签名HMAC值
        h = hmac.new(access_key_secret + "&", string_to_sign, sha1)
        # 按照base64编码规则把HMAC值转为字符串，即签名值
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def composeURL(self):
        # 请求时间戳
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        # 使用uuid生成随机数
        parameters = { \
                'Format'        : 'JSON', \
                'Version'       : '2014-05-15', \
                'AccessKeyId'   : self.access_key_id, \
                'SignatureVersion'  : '1.0', \
                'SignatureMethod'   : 'HMAC-SHA1', \
                'SignatureNonce'    : str(uuid.uuid1()), \
                'TimeStamp'         : timestamp, \
                'LoadBalancerId'    : self.slb_id, \
                'Action'            : self.action, \
                'BackendServers'    : self.action_value_string
        }
        # 把签名值写到字典中
        signature = self.computeSignature(parameters, self.access_key_secret)
        # print "signature:",signature
        parameters['Signature'] = signature
        # 使用urlencode函数把k-v键值转换成这种格式Timestamp=343434&SignatureVersion=1.0
        url = self.slb_server_address + "/?" + urllib.urlencode(parameters)
        return url

    def execURL(self):
        res = urllib.urlopen(self.composeURL())
        return res.read()

if __name__ == '__main__':
    f = BackendServers()
    result = f.execURL()
    if "Code" in result:
        print("权重值设置失败！")
        print(result)
        sys.exit(2)
    else:
        print("权重值修改成功.")
