
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def main():
    filename = "D:\\resource\\CNVD-CRAWLER\\t_cnvd_part_1.sql"
    sendData = {"file": open(filename, "rb")}
    datagen, headers = multipart_encode(sendData)
    request = urllib2.Request("http://192.168.10.130:8060/posttest/servlet/uploadFileServlet", datagen, headers)
    # jsondata = urllib2.urlopen(request).read()

if __name__ == '__main__':
    main()