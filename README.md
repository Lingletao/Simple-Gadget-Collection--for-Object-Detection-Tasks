# Simple Gadget Collection-for-Object Detection Tasks
* Automatic image annotation
* Conversion between different annotation formats
* Obtain statistical information about your dataset

This is a simple collection of gadgets for regular **object detection** tasks. You can also modify it yourself to implement your ideas. It is very simple to use, you just need to copy the python file you need to use, and specify the relevant parameters, and execute it. Please read the following tutorial carefully before using it.

## 1. Automatic image annotation：
`auto_annotate_mmdetect.py`  
This tool is to help you complete a large number of labeling tasks quickly. It is based on the object detection model trained by [mmdetection](https://github.com/open-mmlab/mmdetection).   
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


## 2.Conversion between different annotation formats:
### 2.1 PASCAL VOC-->COCO:  
`voc2coco.py`  
The annotation file format generated using [labelImg](https://github.com/tzutalin/labelImg) is usually  [PASCAL VOC](host.robots.ox.ac.uk/pascal/VOC/) (xml) or YOLO(txt). When using many model training suites (e.g. mmdetection), you need to convert the xml files to [COCO](https://cocodataset.org)(json).  
**Usuage:**  
**Step1:** copy `voc2coco.py` to VOC dataset folder that you are going to transfer (as shown below).
```
Before:
dataset_VOC
  ├─ImageSets
  │  └─Main
  │     ├─train.txt
  │     ├─val.txt
  │     └─trainval.txt
  ├─Annotations    <--xml files are put there
  ├─JPEGImages     <--images are put there
  └─voc2coco.py    <--you should put it here
```
**Step2:** excute `voc2coco.py`. The images will be automatically copied to the specified folder. You only need to change the name of the dataset manually.
```
After:
dataset_COCO   <--You only need to change the name of the dataset manually
  ├─train     <--images for training are copied there
  ├─val       <--images for valuation are copied there
  ├─train.json
  └─val.json
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
This tool is used to solve the problem of converting COCO dataset format (json) to [YOLO](https://github.com/ultralytics/yolov5) format (txt).  
**Usuage:**  
**Step1:** copy `coco2yolov5.py` to the coco dataset folder that you are going to transfer. (As show below↓)  
```
Before:
dataset_coco
  ├─train.json        <--annotation json file (for training)
  ├─val.json          <--annotation json file (for valuation)
  ├─train             <--images are saved here (for training)
  ├─val               <--images are saved here (for valuation)
  └─coco2yolov5.py    <--you should put it here
```
**Step2:** specify the dataset name in `coco2yolov5.py`.
```
dataset_name = 'dataset'                  # specify your dataset name
dataset_name = dataset_name + '_yolo'
```
**Step3:** excute `coco2yolov5.py`.
```
After:
dataset_yolo
├─train┬images      <--images are saved here (for training)
│       └labels      <--annotation txt file (for training)
│
└─val┬─images      <--images are saved here (for valuation)
       └─labels      <--annotation txt file (for valuation)
```

## 3. Obtain statistical information about your dataset:  
### 3.1 Simple statistical information:
These tools provide statistical methods for different formats of annotation files. You can use the statistical tools to quickly understand the percentage of each sample and determine whether the samples are balanced with each other, providing useful information for your next training and fine-tuning.

`xml_cls_stat.py` and `json_cls_stat.py` to obtain the statistical information of the annotation file in VOC and COCO format respectively. The usage method is very simple, you need to copy `xml_cls_stat.py` or `json_cls_stat.py` to your VOC or COCO data set folder.  
It should be noted that the annotation files and images in the VOC format are stored uniformly, and `xml_cls_stat.py` counts the information of the entire dataset. And to use `json_cls_stat.py` you need to specify whether to count `train` or `val`.  
`json = json.load(open('train.json'))  # Specify train.json`  
Then execute it, you can get statistics of all categories and the number of instances. (As show below↓)
```
=======Statistic Details===========
Class Name: DC, Class ID: 2455, Instances: 865
Class Name: HC, Class ID: 2448, Instances: 383
Class Name: WJ, Class ID: 2449, Instances: 696
```
### 3.2 Find pictures that contain the specified class 
`xml_find_picture.py` and `json_find_picture.py`. The usage is exactly the same and very simple, you only need to copy it to the VOC data set folder. Specify the name of the category you need to find,
`specified_name ='WJ'`   
Finally, execute it.   
The program will print out the file name containing the specified class, and show how many pictures in total contain the class you specified. (As show below↓)
```
···
machinery561.xml
machinery394.xml
machinery394.xml
machinery225.xml
machinery084.xml
There are 881 pictures contain specified category, (CateName=WJ)
```

## 4. Modify your dataset:  
__NOTE: I recommend that you back up your data before proceeding to avoid tragedy.__
### 4.1 Remove specified class
`xml_cls_del.py`  
Sometimes you will need to delete some special classes, and the workload of manually deleting specified classes is very huge. When you encounter this situation, you can use this tool to delete certain classes you don't need.  
Copy `xml_cls_del.py` to your folder, specify the class you want to delete, and finally execute it.   
Don't worry, the program will automatically create a folder called ‘New_Annotation’ to store these modified annotation files, and your original annotation files will not be affected in any way. 
```
specified_class_name = 'WJ'  # Specify the name of the class to be deleted  
```
Finally, the program will tell you how many instances have been deleted. (As show below↓)
```
There are 648 objects have been removed.
```

### 4.2 Modify the name of the specified class
`xml_cls_namechange.py` or `json_cls_namechange.py`   
The tools of the VOC (xml) version and COCO (json) version are provided here, and they are used in the same way. When you need to modify the name of a certain class or merge certain classes, you can use it to achieve. 
Don't worry, the program will automatically create a folder called ‘New_Annotation’ to store these modified annotation files, and your original annotation files will not be affected in any way.  
Like other tools, you only need to copy `xml_cls_namechange.py` or `json_cls_namechange.py` to your dataset folder, 
and specify your json file save path:  
 ```
json_path = './train.json'	    	#json file path before modification
json_save_path = './train2.json'	#Modified json file save path 
```
specify the name of the class you want to modify, and then execute it. 
```
specified_cls_name = "A" 		    #Class name to be modified 
new_name = "AA"	    	 	        #New class name 
 ```

## 5. Simple image data enhancement:  
`simple_data_enhancement.py`
Specify the folder that needs data enhancement, then select the enhancement method you need to use according to your needs, and finally execute it.   
The tool provides 6 common methods: rotate, flip, brighten, darken, salt and pepper noise, and Gaussian noise. For unneeded methods, just turn their code into comments.  
`file_dir = r'../data/img/'  # Specify the folder that needs data enhancement`
  

## 6. Use models for inference (prediction):  
`infer_by_folder_mmdetection.py`  



## 7. Cascade of models:  
[Examples of practical application of model cascade](https://github.com/Lingletao/Simple-Gadget-Collection--for-Object-Detection-Tasks/blob/main/Picture0.png)
`infer_paddle_2stages.py`
`infer_mmdet_2stages.py`
