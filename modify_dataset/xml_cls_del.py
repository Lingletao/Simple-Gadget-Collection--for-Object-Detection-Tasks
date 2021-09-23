import os
import xml.etree.ElementTree as ET
input_dir = './Annotations'
new_dir = './NewAnnotations'

m = 0
n = 0
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    new_path = os.path.join(new_dir, filename)
    dom = ET.parse(file_path)
    root = dom.getroot()
    for obj in root.iter('object'):
        if obj.find('name').text == 'DZ_A00':
            root.remove(obj)
            n = n + 1
            dom.write(new_path, xml_declaration=True)
    m = m + 1
print("There are %d objects has been removed." % n)
