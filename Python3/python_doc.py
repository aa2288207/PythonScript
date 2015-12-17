from win32com import client as wc
word = wc.Dispatch('Word.Application')
doc = word.Documents.Open('E:\\zxl\\4\\电子版赞美诗400首.doc')
print(doc)
doc.SaveAs('E:\\zxl\\r', 2)
doc.Close()
word.Quit()