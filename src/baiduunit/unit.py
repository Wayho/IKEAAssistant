# coding:utf-8
'''
Created on 2017年7月15日

@author: Administrator
'''
import json

from utils.http_request import HttpRequest


class BaiduUnit(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # token获取(使用应用名称为：“商品导购”)
        self.token_request = HttpRequest("https://aip.baidubce.com/oauth/2.0/token")
        self.key_grant_type = "grant_type"
        self.val_grant_type = "client_credentials";
        self.key_client_id = "client_id"
        self.val_client_id = "CwMUqtG0PlTtwExfLbeBr7qV"
        self.key_client_secret = "client_secret"
        self.val_client_secret = "kZiWVLLjkXo3DOSB8nEglsjgmmyaLFOr"

        # token(9th-November-2017)
        self.val_token = "24.a0ca819335901b0d44ba42ffdbc54532.2592000.1512877347.282335-10028417"

        self.unit_requet = HttpRequest(
            "https://aip.baidubce.com/rpc/2.0/solution/v1/unit_utterance?access_token=" + self.val_token)

    def get_token(self):
        '''
        获取token
        :return: token
        '''
        data = {self.key_grant_type: self.val_grant_type, \
                self.key_client_id: self.val_client_id, \
                self.key_client_secret: self.val_client_secret}
        res = self.token_request.get(params=data).text
        res_dic = json.loads(res)
        if (res_dic.has_key("access_token")):
            return res_dic["access_token"]
        else:
            return None

    def query_request(self, scene_id, query, session_id):
        '''
            用户query请求
            scene_id：场景ID
            query：用户query
            session_id：session ID
        '''
        data = {"scene_id": scene_id, \
                "query": query, \
                "session_id": session_id}

        return self.unit_requet.post(json.dumps(data))
