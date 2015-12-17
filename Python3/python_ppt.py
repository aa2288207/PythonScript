

import os
import win32com
from win32com.client import Dispatch, constants
ppt = win32com.client.Dispatch('PowerPoint.Application')
ppt.Visible = 1

sql = 'insert into hymn(hid,title,content) value("%s", "%s", "%s");\n'
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
                    if shape_count > 1:
                        if pptSel.Slides(i).Shapes(1).HasTextFrame:
                            tmp = pptSel.Slides(i).Shapes(1).TextFrame.TextRange.Text
                            s1 = tmp[tmp.find('首')+1:]
                            s1 = s1.strip()
                            s0 = tmp[:tmp.find('首')]
                            s0 = s0.strip()
                        s2 = ""
                        for j in range(2,shape_count + 1):
                            if pptSel.Slides(i).Shapes(j).HasTextFrame:
                                s2 = '%s%s' % (s2, pptSel.Slides(i).Shapes(j).TextFrame.TextRange.Text)
                    elif shape_count == 1:
                        s1 = ""
                        s2 = pptSel.Slides(i).Shapes(1).TextFrame.TextRange.Text
                    else:
                        f.write('-----------------------\n')
                        print(shape_count)
                        print('--------------------------')
                    f.write(sql % (s0, s1, s2))
                except Exception as e:
                    f.write('------%s\n' % e)
                    
            f.close()
except Exception as e:
    print(e)
finally:
    ppt.Quit()
    
