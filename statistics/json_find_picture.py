import sys, os, urllib3
import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from numpy import *

specified_name = 'WJ'

# specified_id = 1

json = json.load(open('train.json'))
diction_images = json['images']
diction_categories = json['categories']
diction_annotations = json['annotations']

for item in diction_categories:
    if specified_name == item['name']:
        specified_id = item['id']

picture_id_list = []
for item in diction_annotations:
    if specified_id == item['category_id']:
        picture_id = item['image_id']
        picture_id_list.append((picture_id))
# print(picture_id_list)
number_picture = len(picture_id_list)
image_list = []
for item in diction_images:
    i = 0
    for i in range(number_picture):
        if picture_id_list[i] == item['id']:
            file_name = item['file_name']
            print(file_name)
            image_list.append((file_name))
            i = i + 1

print("There are {} pictures contain specified category.(CateName: {} CateID: {})".format(number_picture, specified_name, specified_id))
