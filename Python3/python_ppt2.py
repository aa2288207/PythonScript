

import os
import win32com
from win32com.client import Dispatch, constants
ppt = win32com.client.Dispatch('PowerPoint.Application')
ppt.Visible = 1

sql = 'insert into hymn(title,content) value("%s", "%s");\n'
rootdir = 'E:\\zxl\\1'
try:
    for parent, dirs, filenames in os.walk(rootdir):
        for filename in filenames:
            path = os.path.join(parent,filename)
            f = open('E:\\zxl\\r\\%s.txt' % filename, 'w')

            pptSel = ppt.Presentations.Open(path)
            # win32com.client.gencache.EnsureDispatch('PowerPoint.Application')

            #get the ppt's pages
            slide_count = pptSel.Slides.Count
            for i in range(1,slide_count + 1):
                shape_count = pptSel.Slides(i).Shapes.Count
                try:
                    if shape_count == 2:
                        if pptSel.Slides(i).Shapes(1).HasTextFrame:
                            s1 = pptSel.Slides(i).Shapes(1).TextFrame.TextRange.Text
                            s1 = s1[s1.find(' ')+1:]
                            s1 = s1.strip()
                        if pptSel.Slides(i).Shapes(2).HasTextFrame:
                            s2 = pptSel.Slides(i).Shapes(2).TextFrame.TextRange.Text
                        print(sql % (s1, s2))
                        f.write(sql % (s1, s2))
                    else:
                        f.write('-----------------------\n')
                        print(shape_count)
                        print('--------------------------')
                except Exception as e:
                    f.write('------%s\n' % e)
                    
            f.close()
except Exception as e:
    print(e)
finally:
    ppt.Quit()
    
