# Simple-toolbox-for-Object-detection-tasks
Automatic labeling, conversion of different data set formats, sample size statistics, model cascade  

This is a simple collection of tools for converting annotation file formats for computer vision object detection. The usage method is very simple, you only need to copy the py script file to the folder you need to convert, modify the script, and specify the parameters you need. Please refer to the tutorial for detailed usage. 

## 1. Automatic image annotation：
`auto_annotate_mmdetect.py`  
This tool is to help you complete a large number of labeling tasks quickly. It is based on the target detection model trained by [mmdetection](https://github.com/open-mmlab/mmdetection).   
**Usuage:**  
**Step1:** you need to use mmdetection and a small amount of **labeled data** (about 200~300 images) to train to get a rough object detection model(e.g. Faster-RCNN: [faster_rcnn_r50_fpn_1x_coco.py](https://github.com/open-mmlab/mmdetection/tree/master/configs/faster_rcnn)). If you don't know how to use mmdetection to train a object detection model, I strongly suggest you read the [tutorial](https://github.com/open-mmlab/mmdetection/blob/master/docs/2_new_data_model.md) on mmdetection first.  
**Step2:** use `auto_annotate_mmdetect.py` to mark the remaining large amount of unmarked data and generate a VOC format (xml) file. Before that, you need to modify some places to specify the name of the annotation object and the place where the annotation file is saved.   

```
files_path = '../project/mmdetection/data/image'              # The path of the image folder to be annotated  
img_save_path = './results'                                   # The path of the annotated images to be saved  
xml_save_path = './Annotations'                               # The path of the image annotation files (xml) to be saved  
cfg = './faster_rcnn_r50_fpn_1x_coco.py'                      # Your model configure file (mmdetection)  
wgt = './epoch_12.pth'                                        # Your model weight file  
device = 'cuda:0'                                             # Use GPU  
class_dic = {'0': 'cat',
             '1': 'dog',  
             '2': 'rabbit',  
             '3': 'mouse'}                                    # Class ID --> Class name  
```
**Step3:** `auto_annotate_mmdetect.py`, which will automatically use the model you just trained to generate the corresponding annotation files(xml).               
**Step4:** you can use [labelImg](https://github.com/tzutalin/labelImg) to **manually** correct the automatically generated files.   


## 2.Conversion of different data set annotation formats:
### 2.1 VOC-->COCO:  
`voc2coco.py`  
The annotation file format generated using [labelImg](https://github.com/tzutalin/labelImg) is usually VOC(xml) or YOLO(txt). When using many model training suites (e.g. mmdetection), you need to convert the xml files to COCO(json).  
**Usuage:**  
**Step1:** copy `voc2coco.py` to VOC dataset folder that you are going to transfer (as shown below).
```
  Before:
  dataset_VOC
  |--ImageSets
  |  |--Main
  |     |--train.txt
  |     |--val.txt
  |     |--trainval.txt
  |--Annotations    <--xml files are put there
  |--JPEGImages     <--images are put there
  |--voc2coco.py    <--you should put it here 
```
**Step2:** excute `voc2coco.py`. The images will be automatically copied to the specified folder. You only need to change the name of the dataset manually.
```
After:
dataset_COCO   <--You only need to change the name of the dataset manually
  |--train     <--images for training are copied there
  |--val       <--images for valuation are copied there
  |--train.json
  |--val.json
```  
By the way, it will automatically count information about the kinds your dataset contains and the number of its instances.(like this ↓)  
```
=======Statistic Details===========  
Class Name: green_net, Instances: 119  
Class Name: obj, Instances: 522  
Class Name: kite, Instances: 152  
===================================  

========Create train.json DONE========  
Foud 3 categories: dict_keys(['obj', 'kite', 'green_net']) --> your predefine categories 3: dict_keys(['green_net', 'obj', 'kite'])  
Category: id --> {'green_net': 783, 'obj': 793, 'kite': 792}  
=====================================  

========Create val.json DONE========  
Foud 3 categories: dict_keys(['obj', 'kite', 'green_net']) --> your predefine categories 3: dict_keys(['green_net', 'obj', 'kite'])  
Category: id --> {'green_net': 783, 'obj': 793, 'kite': 792}  
=====================================

========Coco Dataset Details========  
Training set size: 516  
Valuation set size: 130  
```  
  
### 2.2 COCO-->YOLO:  

`coco2yolov5.py`
This tool is used to solve the problem of converting COCO dataset format (json) to YOLO format (txt).  
**Usuage:**  
**Step1:** copy `coco2yolov5.py` to the coco dataset folder that you are going to transfer (as shown below).  
```
Before:
--dataset_coco
|--train.json        <--annotation json file (for training)
|--val.json          <--annotation json file (for valuation)
|--train             <--images are saved here (for training)
|--val               <--images are saved here (for valuation)
|--coco2yolov5.py    <--you should put it here
```
**Step2:** specify the dataset name in `coco2yolov5.py`.
```
dataset_name = 'test_XXX'                  # specify your dataset name
dataset_name = dataset_name + '_yolo'
```
**Step3:** excute `coco2yolov5.py`.
```
After:
--dataset_yolo
|--train--images      <--images are saved here (for training)
|       |-labels      <--annotation txt file (for training)
|
|--val----images      <--images are saved here (for valuation)
        |-labels      <--annotation txt file (for valuation)
```

image_cropping.py

image_data_enhancement.py

img_crop_by_xml.py

infer_paddle_2stages.py

inference_mmdet_2stages.py

json_cls_namechange.py

json_cls_stat.py

json_find_picture.py



prediction_stat_mmdet.py



xml_cls_del.py

xml_cls_namechange.py

xml_cls_stat.py

xml_find_picture.py
