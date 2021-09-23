# usuage:
# Step1: copy this tool script to the coco dataset folder that you are going to transfer (as shown below).
# Step2: specify the dataset name, and run this script.
# Before:
# --dataset_coco
#   |--train.json <--annotation json file (for training)
#   |--val.json   <--annotation json file (for valuation)
#   |--train      <--images are saved here (for training)
#   |--val        <--images are saved here (for valuation)
#   |--coco2yolov5.py <--you should put your tool here
# After:
# --dataset_yolo
#   |--images--train-- <--images are saved here (for training)
#   |       |--val <--images are saved here (for valuation)
#   |
#   |--labels--train----annotation txt file (for training)
#           |--val <--annotation txt file (for valuation)


import os
import json
from tqdm import tqdm
import argparse
import shutil

dataset_name = 'test_XXX' # specify your dataset name
dataset_name = dataset_name + '_yolo'

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] + box[2] / 2.0
    y = box[1] + box[3] / 2.0
    w = box[2]
    h = box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def anno_conv(json_file, ana_root_save_path, img_save_path):
    json_file_name = json_file.split('/')[-1]
    json_file_name = json_file_name.split('.')[0]

    data = json.load(open(json_file, 'r'))
    if not os.path.exists(ana_root_save_path):
        os.makedirs(ana_root_save_path)

    ana_txt_save_path = os.path.join(ana_root_save_path, json_file_name)
    if not os.path.exists(ana_txt_save_path):
        os.makedirs(ana_txt_save_path)
    if not os.path.exists(image_save_path_train):
        os.makedirs(image_save_path_train)
    if not os.path.exists(image_save_path_val):
        os.makedirs(image_save_path_val)

    id_map = {}
    with open(os.path.join(ana_root_save_path, 'classes.txt'), 'w') as f:
        for i, category in enumerate(data['categories']):
            f.write(f"{category['name']}\n")
            id_map[category['id']] = i

    for img in tqdm(data['images']):
        filename = img["file_name"]
        img_width = img["width"]
        img_height = img["height"]
        img_id = img["id"]
        head, tail = os.path.splitext(filename)
        ana_txt_name = head + ".txt"
        f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')
        file_name = './' + json_file_name
        # print(filename)
        shutil.copy(os.path.join(file_name, filename), os.path.join(img_save_path, filename))
        for ann in data['annotations']:
            if ann['image_id'] == img_id:
                box = convert((img_width, img_height), ann["bbox"])
                f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], box[0], box[1], box[2], box[3]))
        f_txt.close()

json_file_train = './train.json'
json_file_val = './val.json'
annotation_save_path_train = '../' + dataset_name + '/labels/'
image_save_path_train = '../' + dataset_name + '/images/train'
annotation_save_path_val = '../' + dataset_name + '/labels/'
image_save_path_val = '../' + dataset_name + '/images/val'

anno_conv(json_file_train, annotation_save_path_train, image_save_path_train)
anno_conv(json_file_val, annotation_save_path_val, image_save_path_val)
