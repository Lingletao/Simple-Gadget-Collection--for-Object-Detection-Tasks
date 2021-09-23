import os
input_dir='./Annotations'
import xml.etree.ElementTree as ET

specified_name = 'WJ'

picture_name_list = []
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    dom = ET.parse(file_path)
    root = dom.getroot()
    for obj in root.iter('object'):
        if obj.find('name').text == specified_name:
            picture_name_list.append((filename))
            print(filename)


print("There are {} pictures contain specified category, (CateName={})".format(len(picture_name_list), specified_name))
