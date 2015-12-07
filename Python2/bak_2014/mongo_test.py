# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('172.16.2.3', 27017)
client.admin.authenticate('analysis', 'system12#34*')

db = client.cuckoo

c_analysis = db.analysis
c_calls = db.calls

def function1():
    analysis_data = c_analysis.find_one({'info.id': 3})

    print('-1'*12)
    print analysis_data["signatures"]
    print('-2'*12)
    for sign in analysis_data["signatures"]:
        print sign["data"]
        for data in sign["data"]:
            for (key, value) in data.items():
                print key, value

    print('-3'*12)
    for ad in analysis_data:
        print ad

    print '*'*12


def main2():
    for process in analysis_data["behavior"]["processes"]:
        for call in process["calls"]:
            f_calls = c_calls.find_one({"_id":call})
            print f_calls
            return

def function2():
    analysis_data = c_analysis.find_one({'info.id': 11})
    for file in analysis_data["behavior"]["summary_extend"]["files"]:
        print file[0].encode('utf-8')
        print file[1].encode('utf-8')

def function3():
    analysis_data = c_analysis.find_one({'info.id': 297})
    for processes in analysis_data["behavior"]["signatures"]:
        print ('xx===%s' % type(analysis_data["behavior"]))
        print ('first:%s' % processes)
        print (type(processes))
        for process in analysis_data["behavior"]["signatures"][processes]:
            print (process)
            # for sign in analysis_data["behavior"]["signatures"][processes][process]['data']:
            #     for i in sign:
            #         print i, sign[i]
            # for pro in process:
            #     print pro
                # for sign in analysis_data["behavior"]["signatures"][processes][process][pro].data:
                #     print 'three:%s' % sign
                #     for key, value in sign.items:
                #         print key ,value

def function4():
    analysis_data = c_analysis.find_one({'info.id': 620})
    print analysis_data['target']['marks']
    print analysis_data['target']['file']['rop']

if __name__ == '__main__':
    function4()
        


