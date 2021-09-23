import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET
from collections import Counter
import xml.dom.minidom
from shutil import move
'''
Usuage:
The format of original dataset is shown as follows:
Dataset_VOC
    |--ImageSets
    |  |--Main
    |     |--train.txt
    |     |--val.txt
    |     |--trainval.txt
    |--Annotations  <--xml files are put there
    |--JPEGImages   <--images are put there
    
The format of converted dataset is shown as follow:
Dataset_COCO
    |--train  <--images for training are copied there
    |--val    <--images for valuation are copied there
    |--train.json
    |--val.json
'''

path2 = "."
START_BOUNDING_BOX_ID = 1

train_ratio = 0.8
save_json_train = 'train.json'
save_json_val = 'val.json'
xml_dir = "Annotations"
img_dir = "JPEGImages"

def get(root, name):
    return root.findall(name)

def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def convert(xml_list, json_file):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = pre_define_categories.copy()
    bnd_id = START_BOUNDING_BOX_ID
    all_categories = {}
    for index, line in enumerate(xml_list):
        # print("Processing %s"%(line))
        xml_f = line
        tree = ET.parse(xml_f)
        root = tree.getroot()

        filename = os.path.basename(xml_f)[:-4] + ".jpg"
        image_id = 1 + index
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width, 'id': image_id}
        # image = {'height': height, 'width': width, 'id': image_id}
        json_dict['images'].append(image)

        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category in all_categories:
                all_categories[category] += 1
            else:
                all_categories[category] = 1
            if category not in categories:
                if only_care_pre_define_categories:
                    continue
                new_id = len(categories) + 1
                print(
                    "[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(
                        category, pre_define_categories, new_id))
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))
            ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))
            xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
            ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
            assert (xmax > xmin), "xmax <= xmin, {}".format(line)
            assert (ymax > ymin), "ymax <= ymin, {}".format(line)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width * o_height, 'iscrowd': 0, 'image_id':
                image_id, 'bbox': [xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict, indent=1)
    json_fp.write(json_str)
    json_fp.close()
    print("========Create {} DONE========".format(json_file))
    print("Foud {} categories: {} --> your predefine categories {}: {}".format(len(all_categories),
                                                                                  all_categories.keys(),
                                                                                  len(pre_define_categories),
                                                                                  pre_define_categories.keys()))
    print("Category: id --> {}".format(categories))
    # print(categories.keys())
    # print(categories.values())
    print('=====================================' + '\n')


if __name__ == '__main__':

    classes = []
    for filename in os.listdir(path2 + '/' + xml_dir):
        file_path = os.path.join(path2 + '/' + xml_dir, filename)
        dom = ET.parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):
            label = obj.find('name').text
            classes.append((label))
            count = Counter(classes)

    print("Number of all categories:", len(count))
    keys = list(count.keys())
    value = list(count.values())

    print("=======Statistic Details===========")
    i = 0
    for i in range(len(count)):
        print("Class Name: {}, Instances: {}".format(keys[i], value[i]))
        i = i + 1
    print('===================================' + '\n')

    pre_define_categories = {}

    for i, cls in enumerate(classes):
        pre_define_categories[cls] = i + 1
    only_care_pre_define_categories = True

    xml_list = glob.glob(xml_dir + "/*.xml")
    xml_list = np.sort(xml_list)
    
    np.random.seed(100)
    np.random.shuffle(xml_list)

    train_num = int(len(xml_list) * train_ratio)
    xml_list_train = xml_list[:train_num]
    xml_list_val = xml_list[train_num:]

    convert(xml_list_train, save_json_train)
    convert(xml_list_val, save_json_val)

    if os.path.exists(path2 + "/Dataset_COCO/train"):
        shutil.rmtree(path2 + "/Dataset_COCO/train")
    os.makedirs(path2 + "/Dataset_COCO/train")
    if os.path.exists(path2 + "/Dataset_COCO/val"):
        shutil.rmtree(path2 + "/Dataset_COCO/val")
    os.makedirs(path2 + "/Dataset_COCO/val")

    f1 = open("train.txt", "w")
    for xml in xml_list_train:
        img = path2 + '/' + img_dir + '/' + xml[12:-4] + ".jpg"
        f1.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, path2 + "/Dataset_COCO/train/" + os.path.basename(img))

    f2 = open("val.txt", "w")
    for xml in xml_list_val:
        img = path2 + '/' + img_dir + '/' + xml[12:-4] + ".jpg"
        f2.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, path2 + "/Dataset_COCO/val/" + os.path.basename(img))
    f1.close()
    f2.close()
    move(path2 + '/' + save_json_train, './Dataset_COCO/')
    move(path2 + '/' + save_json_val, './Dataset_COCO/')

    print("========Coco Dataset Details========")
    print("Training set size:", len(xml_list_train))
    print("Valuation set size:", len(xml_list_val))
