
import xml.etree.ElementTree as ET

root_dir = 'F:\\works\\cve\\allitems-cvrf-year-1999.xml'
xmlns = '{http://www.icasi.org/CVRF/schema/vuln/1.1}'
sql = ''

tree = ET.parse(root_dir)
root = tree.getroot()


for child in root.findall('%sVulnerability' % xmlns):
    cve = child.find('%sCVE' % xmlns).text
    for note in child.find('%sNotes' % xmlns):
        if note.get('Type') == 'Description':
            description = note.text
        elif note.get('Title') == 'Published':
            published = note.text
        elif note.get('Title') == 'Modified':
            modified = note.text

    references = []
    if child.find('%sReferences' % xmlns):
        for reference in child.find('%sReferences' % xmlns):
            url = reference.find('%sURL' % xmlns).text
            desc = reference.find('%sDescription' % xmlns).text
            references.append('%s\n%s\n' % (url, desc))

    print('-'*12)
    print('cve: %s' % cve)
    print('description: %s' % description)
    print('published: %s' % published)
    print('modified: %s' % modified)
    print('references: %s' % ''.join(references))
