import os
import xml.etree.ElementTree as ET

input_dir = './Annotations'
new_dir = './New_Annotations/'
os.makedirs(new_dir)

specified_cls_name = "T"
new_name = 'TT'

m = 0
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    dom = ET.parse(file_path)
    root = dom.getroot()
    n = 0
    for obj in root.iter('object'):
        if obj.find('name').text == specified_cls_name:
            obj.find('name').text = new_name
            n = n + 1
    dom.write(new_dir + filename, xml_declaration=True)
    m = m + 1
print("There are %d annotation files has been modified."%m)
