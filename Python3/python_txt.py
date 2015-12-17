
f2 = open("E:\\zxl\\4\\r222.txt", 'w')
with open('E:\\zxl\\4\\r.txt') as f:
    contexts = f.read()
    contexts = contexts.split("\n\n")
    for context in contexts:
        tmps = context.split('\n')
        tmp = tmps[0]
        print(tmp)
        if tmp.find('、') >= 0:
            number = tmp[:tmp.find('、')]
            title = tmp[tmp.find('、')+1:]
        elif tmp.find('首') >= 0:
            number = tmp[:tmp.find('首')]
            title = tmp[tmp.find('首')+1:]
        elif tmp.find(' ') >= 0:
            number = tmp[:tmp.find(' ')]
            title = tmp[tmp.find(' ')+1:]
        else:
            print(tmp)

        texts = []
        count  = len(tmps)
        for x in range(1, count):
             texts.append(tmps[x])

        text = '\n'.join(texts)

        sql = 'insert into hymn(hid,title,content) value("%s", "%s", "%s");\n'
        print(sql % (number, title, text))
        f2.write(sql % (number, title, text))

f2.close()