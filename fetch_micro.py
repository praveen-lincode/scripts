import glob
import os
import re 
import xml.etree.ElementTree as ET
import cv2
# from all_classes import *
import shutil

classes = []

# req_classes = mirco


def create_folder(out = "val"):
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    print(out , ' created!')

for f in range(200):
    count = 0
    path = f'./batch_{f}'
    # path = "/home/lincode/Documents/Gokul/INDO_MIM/notebooks/yolov5/yolov5/annotations/all"
    # path = f'/home/lincode/Documents/Gokul/INDO_MIM/notebooks/yolov3/yolov3/annotations/val'
    # path = f'/home/lincode/Documents/Gokul/INDO_MIM/notebooks/yolov3/yolov3/annotations/XmlToTxt/train_xml_edited'
    for file in glob.glob(os.path.join(path,'*.xml')):
        # print((file.split('/')[-1]).split('.')[0])
        tree = ET.parse(file)
        
        for elt in tree.iter():
            if (elt.tag == 'name'):
                classes.append(elt.text )
            if ((elt.tag == 'name') & ((elt.text in req_classes))):
                img_name =  file.replace(".xml",".jpg")#(file.spilt("/")[-1])
                img = cv2.imread(img_name)
                # print((file.split('/')[-1]).split('.')[0])
                # print(elt.text )
                # elt.text = 'mdv001'

                count += 1
    # # #     tree.find('//filename').text = (file.split('/')[-1]).split('.')[0] + '.jpg' 
            if count >0 :
                f = "train"
                img_name = img_name.replace(f"/batch_{f}/","/crack/")
                print(img_name)
                file = file.replace(f"/batch_{f}/","/crack/")
                tree.write(file)
                cv2.imwrite(img_name ,img)
                count = 0
    if count > 0:
        print(f'batch_{f}')
        print(count)   