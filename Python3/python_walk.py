import os


rootdir = 'E:\\zxl\\txt歌词'

for parent, dirs, filenames in os.walk(rootdir):
    for filename in filenames:
        print(os.path.join(parent,filename))