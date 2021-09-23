import xml.dom.minidom
import torch
from mmdet.apis import init_detector, inference_detector
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os

files_path = '/home/ling/project/mmdetection/drone_inf/image' # The path of the image folder to be annotated
img_save_path = './results'                                   # The path of the annotated images to be saved
xml_save_path = './Annotations'                               # The path of the image annotation files to be saved
cfg = './faster_rcnn_r50_fpn_1x_coco.py'                      # Your model configure file
wgt = './epoch_12.pth'                                        # Your weight file
device = 'cuda:0'                                             # Use GPU
class_dic = {'0': 'jueyuanzi',
             '1': 'naizhang_xianjia',
             '2': 'xuanchui_xianjia',
             '3': 'binggou_xianjia'}                          # Class ID --> Class name

# model build, you must build model first.
def model_build(cfg, wgt, device):
    model = init_detector(cfg, wgt, device=device)
    return model

# prediction function
# results are shown as torch tensor:
# tensor([[obj1_x1, obj1_y1, obj1_x2, obj1_y2, obj1_class_id, obj1_confidence],
#         [obj2_x1, obj2_y1, obj2_x2, obj2_y2, obj2_class_id, obj2_confidence]])

def prediction(model, input_dir):
    result_list = []
    img = input_dir
    result = inference_detector(model, img)
    result_dic = []
    objects = []
    # print(result.shape)
    # print(result)
    # print(len(result))
    for i in range(len(result)):
        class_id = i
        for object in result[i]:
            o = [object[0], object[1], object[2], object[3], int(class_id), object[4]]
            objects.append(o)
            result_dic = objects
    result = torch.Tensor(result_dic)
    result_list.append(result)
    result_tensor = torch.cat(result_list, dim=0).reshape(-1, 6)
    # print(result_tensor)
    return result_tensor

# drawing rectangles:
def rectangle_draw(file_path, sgl_img_rst, colour, width):
    taking_img = Image.open(file_path)
    draw = ImageDraw.Draw(taking_img)
    for i in range(sgl_img_rst.shape[0]):
        draw.rectangle((sgl_img_rst[i][0],
                        sgl_img_rst[i][1],
                        sgl_img_rst[i][2],
                        sgl_img_rst[i][3]),
                       outline=colour, width=width)
    plt.imshow(taking_img)
    plt.show()
    return taking_img

def predict_in_path(files_path, save_path, xml_save_path, cfg, wgt, device, class_dic):
    sheet = []
    positive = 0

    model = model_build(cfg, wgt, device)

    for filename in os.listdir(files_path):
        file_path = os.path.join(files_path, filename)
        sgl_img_rst = prediction(model, file_path)
        # print("Image Name:", filename)
        # print("Corona Number:", sgl_img_rst.shape[0])
        # count the number
        if sgl_img_rst.shape[0] != 0:
            positive = positive + 1
        taking_img = rectangle_draw(file_path, sgl_img_rst, 'red', 5)
        save_name = str(save_path + '/' + 'INF_RST_' + filename)
        taking_img.save(save_name)
        # print('image is saved in: ', save_name)
        # print("Current corona number:", positive)
        xml_generator(file_path, sgl_img_rst, xml_save_path, class_dic)
    return sheet, positive

def result2dic_list(result_tensor):
    object_list = []
    result = result_tensor.tolist()
    for obj in result:
        object = {'name': '', 'confidence': '', 'xmin': '', 'ymin': '', 'xmax': '', 'ymax': ''}
        object['xmin'] = obj[0]
        object['ymin'] = obj[1]
        object['xmax'] = obj[2]
        object['ymax'] = obj[3]
        object['name'] = obj[4]
        object['confidence'] = obj[5]
        object_list.append(object)
    return object_list

def xml_generator(file_path, result, xml_save_path, class_dic):
    doc = xml.dom.minidom.Document()
    root = doc.createElement('annotation')
    doc.appendChild(root)

    img = Image.open(file_path)
    folder = file_path.split('/')[-2]
    filename = file_path.split('/')[-1]
    path = file_path
    source = 'Unknown'
    width = str(img.width)
    height = str(img.height)
    depth = str(len(img.split()))
    segmented = str(0)

    nodefolder = doc.createElement('folder')
    nodeFilename = doc.createElement('filename')
    nodePath = doc.createElement('path')
    nodeSource = doc.createElement('source')
    nodeSize = doc.createElement('size')
    nodeWidth = doc.createElement('width')
    nodeHeight = doc.createElement('height')
    nodeDepth = doc.createElement('depth')
    nodeSegmented = doc.createElement('segmented')


    nodefolder.appendChild(doc.createTextNode(folder))
    nodeFilename.appendChild(doc.createTextNode(filename))
    nodePath.appendChild(doc.createTextNode(path))
    nodeSource.appendChild(doc.createTextNode(source))
    nodeSegmented.appendChild(doc.createTextNode(segmented))
    nodeWidth.appendChild(doc.createTextNode(width))
    nodeHeight.appendChild(doc.createTextNode(height))
    nodeDepth.appendChild(doc.createTextNode(depth))

    nodeSize.appendChild(nodeWidth)
    nodeSize.appendChild(nodeHeight)
    nodeSize.appendChild(nodeDepth)

    root.appendChild(nodefolder)
    root.appendChild(nodeFilename)
    root.appendChild(nodePath)
    root.appendChild(nodeSource)
    root.appendChild(nodeSize)
    root.appendChild(nodeSegmented)

    object_list = result2dic_list(result)
    for i in object_list:
        # create nodes
        nodeObject = doc.createElement('object')
        nodeName = doc.createElement('name')
        nodeBndbox = doc.createElement('bndbox')
        nodexmin = doc.createElement('xmin')
        nodeymin = doc.createElement('ymin')
        nodexmax = doc.createElement('xmax')
        nodeymax = doc.createElement('ymax')

        # write contents to the nodes

        print(class_dic[str(int(i['name']))])

        nodeName.appendChild(doc.createTextNode(class_dic[str(int(i['name']))]))
        nodexmin.appendChild(doc.createTextNode(str(int(i['xmin']))))
        nodeymin.appendChild(doc.createTextNode(str(int(i['ymin']))))
        nodexmax.appendChild(doc.createTextNode(str(int(i['xmax']))))
        nodeymax.appendChild(doc.createTextNode(str(int(i['ymax']))))

        # append the nodes, construct the architecture.
        nodeObject.appendChild(nodeName)
        nodeObject.appendChild(nodeBndbox)
        nodeBndbox.appendChild(nodexmin)
        nodeBndbox.appendChild(nodeymin)
        nodeBndbox.appendChild(nodexmax)
        nodeBndbox.appendChild(nodeymax)
        root.appendChild(nodeObject)

    fp = open(xml_save_path + '/' + str(filename.split('.')[0]) + '.xml', 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    # print('Annotation xml file is saved in:', xml_save_path + '/' + str(filename.split('.')[0]) + '.xml')

sheet, positive = predict_in_path(files_path, img_save_path, xml_save_path, cfg, wgt, device, class_dic)
