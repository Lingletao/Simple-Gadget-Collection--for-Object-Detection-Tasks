import os
input_dir='./Annotations'
import xml.etree.ElementTree as ET
from collections import Counter
import xml.dom.minidom

class_list = []

for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    dom = ET.parse(file_path)
    root = dom.getroot()
    for obj in root.iter('object'):
        label = obj.find('name').text
        class_list.append((label))
        count = Counter(class_list)

print("Number of all categories:", len(count))
keys = list(count.keys())
value = list(count.values())

print("=======Statistic Details===========")
i = 0
for i in range(len(count)):
    print("Class Name: {}, Instances: {}".format(keys[i], value[i]))
    i = i + 1
