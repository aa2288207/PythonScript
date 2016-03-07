# -*- coding: utf-8 -*-

import urllib2 as u2
from suds.client import Client
from suds.transport.http import HttpTransport
import httplib


class HTTPSClientAuthHandler(u2.HTTPSHandler):
    def __init__(self, key, cert):
        u2.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


class HTTPSClientCertTransport(HttpTransport):
    def __init__(self, key, cert, *args, **kwargs):
        HttpTransport.__init__(self, *args, **kwargs)
        self.key = key
        self.cert = cert

    def u2open(self, u2request):
        tm = self.options.timeout
        url = u2.build_opener(HTTPSClientAuthHandler(self.key, self.cert))
        if self.u2ver() < 2.6:
            socket.setdefaulttimeout(tm)
            return url.open(u2request)
        else:
            return url.open(u2request, timeout=tm)


# These lines enable debug logging; remove them once everything works.
def getClient(url, key, cert):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    logging.getLogger('suds.transport').setLevel(logging.DEBUG)
    c = Client(url, transport=HTTPSClientCertTransport(key, cert))
    return c


def websevicewithcer(url):
    # key文件是从pfx导出的，命令是：openssl pkcs12 -in xxx.pfx -nocerts -nodes -out private.key
    # 这里换成你调用端的私钥文件
    root_dir = 'F:\\works\\CNVD\\'
    key = '%sabc.keystore' % root_dir
    # cer是IE导出的，记得要用Base64编码格式的
    # 这里换成你要调用的网址的客户端证书文件
    cert = '%sabc.truststore' % root_dir
    client = getClient(url, key, cert)
    result = client.service
    return result


def custom_method(param):
    wsdl_url = 'https://127.0.0.1:8443/services/cctvInfo'
    websev = websevicewithcer(wsdl_url)
    # 调用方式websev.方法名（参数）
    ws = websev.getFlawInfo(param)
    return ws

if __name__ == '__main__':
    result = custom_method()
    print(result)
