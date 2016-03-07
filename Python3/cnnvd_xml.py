
import os
import cgi
import codecs
import xml.etree.ElementTree as ET

root_dir = 'F:\\works\\CNNVD\\xml\\'
xmlns = '{http://www.cnnvd.org.cn/vuln/1.0}'
sql = "insert into s_cnnvd \
(`name`,`cnnvd_id`,`published`,`modified`,`source`, \
`severity`,`cnnvd_type`,`thrtype`,`descript`,`solution`,`cve_id`) \
values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');\n"


fs = open('%scnnvd.sql' % root_dir, 'w')
for parent, dirs, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == 'cnnvd.sql':
            continue
        xml_file = os.path.join(parent, filename)
        print(xml_file)
        with codecs.open(xml_file, 'r', 'utf-8') as f:
            txt_xml = f.read()
        # tree = ET.parse(cgi.escape(txt_xml))
        tree = ET.fromstring(cgi.escape(txt_xml, quote=True))
        try:
            for elem in tree.iter(tag='%sentry' % xmlns):
                name_node = elem.find('%sname' % xmlns)
                vuln_id_node = elem.find('%svuln-id' % xmlns)
                published_node = elem.find('%spublished' % xmlns)
                modified_node = elem.find('%smodified' % xmlns)
                source_node = elem.find('%ssource' % xmlns)
                severity_node = elem.find('%sseverity' % xmlns)
                vuln_type_node = elem.find('%svuln-type' % xmlns)
                thrtype_node = elem.find('%sthrtype' % xmlns)
                vuln_descript_node = elem.find('%svuln-descript' % xmlns)
                # vuln_solution_node = elem.find('%svuln-solution' % xmlns)

                cve_id_node = elem.find('%sother-id/%scve-id' % (xmlns, xmlns))
                fs.write(sql % (name_node.text,
                    cve_id_node.text,
                    vuln_id_node.text,
                    published_node.text,
                    modified_node.text,
                    source_node.text,
                    severity_node.text,
                    vuln_type_node.text,
                    thrtype_node.text,
                    vuln_descript_node.text,
                    vuln_solution_node.text))
        except Exception as e:
            print(e)
            
fs.close()