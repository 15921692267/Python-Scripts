#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
import json
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

class SaltAPI():
    def __init__(self):
        self.api_address = 'https://192.168.1.99:8000'
        self.api_user = 'admin'
        self.api_password = 'admin_pass'
    def token(self):
        params = {'eauth':'pam', 'username':self.api_user, 'password':self.api_password}
        url = self.api_address + '/login'
        urlencode = urllib.urlencode(params)
        headers = {'Accept': 'application/json'}     # 默认是json格式，可以不添加这个头信息
        req = urllib2.Request(url, urlencode, headers)
        html = urllib2.urlopen(req)
        content = json.loads(html.read())
        token = content["return"][0]["token"]
        return str(token)
    def execCmd(self, params):
        headers = {'Accept': 'application/json', 'X-Auth-Token':self.token()}
        url = self.api_address + '/'
        urlencode = urllib.urlencode(params)
        req = urllib2.Request(url, urlencode, headers)
        html = urllib2.urlopen(req)
        content = json.loads(html.read())
        return content['return'][0] #.replace('return:\n -',"")
    def allMinion(self):
        params = {'client':'wheel', 'fun':'key.list_all'}
        result = self.execCmd(params)
        minions = result['data']['return']['minions']
        return minions
    def deleteKey(self, node_name):
        params = {'client':'wheel', 'fun':'key.delete', 'match':node_name}
        result = self.execCmd(params)
        return result['data']['success']
    def acceptKey(self, node_name):
        params = {'client':'wheel', 'fun':'key.accept', 'match':node_name}
        result = self.execCmd(params)
        return result
    def execCmdNoArg(self, tgt, fun):
        params = {'client':'local', 'tgt':tgt, 'fun':fun}
        result = self.execCmd(params)
        return json.dumps(result)
    def execCmdArg(self, tgt, fun, arg):
        params = {'client':'local', 'tgt':tgt, 'fun':fun, 'arg':arg}
        result = self.execCmd(params)
        return result
    def execCmdNodeGroup(self, fun, arg, node_group):
        params = {'client':'local', 'fun':fun, 'arg':arg, 'expr_form':node_group}
        result = self.execCmd(params)
        return result
if __name__ == "__main__":
        api = SaltAPI()
        # print api.allMinion()
        # print api.deleteKey('ubuntu')
        # print api.acceptKey('centos7')
        # print api.execCmdNoArg('*', 'grains.items')
        # print api.execCmdArg('*', 'cmd.run', 'df -h')
        # print api.execCmdNodeGroup('cmd.run', 'df -h', 'test')
