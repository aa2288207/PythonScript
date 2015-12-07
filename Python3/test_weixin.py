import sys
import io
import json
import requests

# test_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx6d2e125ead140aef&secret=d4624c36b6795d1d99dcf0547af5443d'
# req = requests.get(test_url)

#get_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx1355b0b502a614de&secret=b553212c75b944cf6a9397e6c2c39e87'
#req = requests.get(get_url)
# access_token = json.loads(req.text)['access_token']
# print(access_token)

access_token = '8_A3XCX_89T66jIplFcZHfn6QQQDEI9DMc0swG5kyb-1LFmmOf6Z5F6yGmwkPdOCVwkb39oB6We8iLrImAu3tHHRXnB5etk8sHfGGD5tXhsDHIjAHAKOP'

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token

data2 = """
 <xml>
 <ToUserName><![CDATA[holdlg]]></ToUserName>
 <FromUserName><![CDATA[oOwaDuFjxsj_gfJbQcdUsAkQWv6Q]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>
"""
r = requests.post(url, data2.encode('utf-8'))
print(r.text)
