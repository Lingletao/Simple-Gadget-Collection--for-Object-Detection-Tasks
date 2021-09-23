# 用于目标检测的简单小工具  
* 自动标注  
* 不同数据集标注格式转换  
* 统计数据集信息  

这是用于常规**目标检测**任务的简单小工具集合。 您也可以自己修改它以实现您的想法。 使用非常简单，只需要复制你需要使用的python文件，指定相关参数，执行即可。 使用前请仔细阅读以下教程。 

## 1. 自动标注：
`auto_annotate_mmdetect.py`  
上万张图像自己一个一个标很烦很累？快使用自动标注吧！  
该工具是为了帮助您快速完成大量的标注任务。 它是基于[mmdetection](https://github.com/open-mmlab/mmdetection)训练的物体检测模型.   
**用法:**  
**Step1:** 首先你需要使用mmdetection和少量**标注过的数据** (最少标注大约200~300张图像)来训练一个粗糙的目标检测模型(如：Faster-RCNN: [faster_rcnn_r50_fpn_1x_coco.py](https://github.com/open-mmlab/mmdetection/tree/master/configs/faster_rcnn)). 如果您不知道如何使用 mmdetection 来训练对象检测模型，强烈建议您阅读 mmdetection的[教程](https://github.com/open-mmlab/mmdetection/blob/master/docs/2_new_data_model.md )
**Step2:** 用脚本`auto_annotate_mmdetect.py`标记剩余的大量未标记数据并生成VOC格式（xml）文件 .在此之前，需要修改一些地方，指定标注对象的名称和标注文件的保存位置。 
```
files_path = '../project/mmdetection/data/image'              # 要被标注的图片文件夹的路径  
img_save_path = './results'                                   # 要被保存的标注图像的路径  
xml_save_path = './Annotations'                               # 要被保存的图像标注文件（xml）的路径  
cfg = './faster_rcnn_r50_fpn_1x_coco.py'                      # 您的模型配置文件 (mmdetection) 
wgt = './epoch_12.pth'                                        # 您的模型权重文件  
device = 'cuda:0'                                             # 使用GPU  
class_dic = {'0': 'cat',
             '1': 'dog',  
             '2': 'rabbit',  
             '3': 'mouse'}                                    # Class ID --> Class name  
```
**Step3:** `auto_annotate_mmdetect.py`会自动使用你刚刚训练的模型来生成相应的标注文件（xml）。              
**Step4:** 你可以使用[labelImg](https://github.com/tzutalin/labelImg) 来**人工矫正（微调）** 那些自动生成的标注文件.   


## 2.不同数据集的标注格式之间的转换:
### 2.1 PASCAL VOC-->COCO:  
`voc2coco.py`  
使用[labelImg](https://github.com/tzutalin/labelImg)生成的标注文件格式通常为[PASCAL VOC](host.robots.ox.ac.uk/pascal/VOC/)(xml)或YOLO( 文本）。 当使用很多模型训练套件（例如mmdetection）时，需要将xml文件转换为[COCO](https://cocodataset.org)(json)。
**用法:**  
**Step1:** 将`voc2coco.py`复制到你要转换的VOC数据集文件夹中（如下图）。
```
转换前:
dataset_VOC
  ├─ImageSets
  │  └──Main
  │     ├──train.txt
  │     ├──val.txt
  │     └──trainval.txt
  ├──Annotations    <--xml文件放在此处  
  ├──JPEGImages     <--图像文件放在此处 
  └──voc2coco.py    <--voc2coco.py文件放在此处 
```
**Step2:** 执行`voc2coco.py`。 图像将自动复制到指定的文件夹。 您只需要手动更改数据集的名称即可。
```
转换后:
dataset_COCO          <--您只需要手动更改数据集的名称即可
  ├──train         <--训练集的图像被复制在此处  
  ├──val           <--验证集的图像被复制在此处    
  ├──train.json
  └──val.json
```  
顺便说一下，它会自动计算关于你的数据集包含的种类和它的实例数量的信息。（像这样↓） 
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
该工具用于解决COCO数据集格式（json）转换为[YOLO]（https://github.com/ultralytics/yolov5)格式（txt）的问题。 
**用法:**  
**Step1:** 将`coco2yolov5.py`复制到你要复制的coco数据集文件夹中（如下图↓）。
```
Before:
dataset_coco
  ├───train.json        <--标注文件json (训练集)
  ├───val.json          <--标注文件json (验证集)
  ├───train             <--存放训练集图像的文件夹  
  ├───val               <--存放验证集图像的文件夹  
  └───coco2yolov5.py    <--`coco2yolov5.py`复制在此处
```
**Step2:** 在 `coco2yolov5.py` 中指定数据集名称。
```
dataset_name = 'dataset'                  # 指定数据集名称
dataset_name = dataset_name + '_yolo'
```
**Step3:** excute `coco2yolov5.py`.
```
After:
dataset_yolo
├──train┬──images        <--存放训练集图像的文件夹
│         └──labels        <--标注文件txt (训练集)
│
└──val┬────images      <--存放验证集图像的文件夹
         └────labels      <--标注文件txt (验证集)
```

## 3. 统计数据集信息 :   
这些工具为不同格式的注释文件提供了统计方法。 您可以使用统计工具快速了解每个样本的百分比，并确定样本之间是否平衡，为您接下来的训练和微调提供有用的信息。 

`xml_cls_stat.py`
`json_cls_stat.py`

## 4. 修改标注文件:  
`xml_cls_del.py`  

`xml_cls_namechange.py`  
`json_cls_namechange.py`  

`xml_find_picture.py`  
`json_find_picture.py`  


## 5. 简单的图像数据增强:  
`image_data_enhancement.py`

## 6. 使用模型进行推理:  
`infer_paddle_2stages.py`


## 7. 级联模型:  
`infer_paddle_2stages.py`
`inference_mmdet_2stages.py`



image_cropping.py

img_crop_by_xml.py





prediction_stat_mmdet.py

