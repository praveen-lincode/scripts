

import glob
# import imageio
# import imgaug as ia
# import imgaug.augmenters as iaa
import numpy as np
import os,shutil
import xml.etree.ElementTree as ET
import xml
import cv2
import xmltodict
import json
import xml.etree.cElementTree as e
import numpy as np
import uuid 
# from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import sys
import time
import threading
from multiprocessing import Process
import random

def create_directory(directory):#create directory
    try:
        os.makedirs(directory)
        print("CREATED>>>>>",directory)
    except:
        print('directory already exists!!')

def read_xml2json(file):
    with open(file) as xml_file:
        my_dict=xmltodict.parse(xml_file.read())
    xml_file.close()
    json_data=json.dumps(my_dict)
    jason = json.loads(json_data)
    # print(file ,'converted to json!')
    return jason



def write_xml(jason,xml_name,dest_path,shape): #converts json to xml and writes xml
    d = jason
    r = e.Element("annotation")
    e.SubElement(r,"folder").text = d['annotation']["folder"]
    e.SubElement(r,"filename").text = d['annotation']["filename"]
    e.SubElement(r,"path").text = str(d['annotation']["path"])
    source_ = e.SubElement(r,"source")
    e.SubElement(source_,'database').text = str(d['annotation']["source"]['database'])
    size_ = e.SubElement(r,"size")
    e.SubElement(size_,'width').text = str(shape[0])#str(d['annotation']["size"]['width'])
    e.SubElement(size_,'height').text = str(shape[0])#str(d['annotation']["size"]['height'])
    e.SubElement(size_,'depth').text = str(d['annotation']["size"]['depth'])


    e.SubElement(r,"segmented").text = str(d['annotation']["segmented"])
    print('shape:',shape)
    if type(jason['annotation']['object']) == list:
        for i,z in enumerate(d['annotation']["object"]):
            # if (((z['bndbox']['xmax']) >= 0) & ((z['bndbox']['ymax']) >= 0)&((z['bndbox']['xmin']) >= 0)&((z['bndbox']['ymin']) >= 0)):
#             if (((z['bndbox']['xmax']) <= shape[1])&((z['bndbox']['ymax']) <= shape[0])):
#                 if (((z['bndbox']['xmax']) >= 0)&((z['bndbox']['ymax']) >= 0)&((z['bndbox']['xmin']) >= 0)&((z['bndbox']['ymin']) >= 0)):
            exec(f'object_{i}= e.SubElement(r,"object")') 
            exec(f'e.SubElement(object_{i},"name").text = str(z["name"])')
            exec(f'e.SubElement(object_{i},"pose").text = str(z["pose"])')
            exec(f'e.SubElement(object_{i},"truncated").text = str(z["truncated"])')
            exec(f'e.SubElement(object_{i},"difficult").text = str(z["difficult"])')
            exec(f'bndbox_{i} = e.SubElement(object_{i},"bndbox")')
            exec(f"e.SubElement(bndbox_{i},'xmin').text = str(z['bndbox']['xmin'])")
            exec(f"e.SubElement(bndbox_{i},'ymin').text = str(z['bndbox']['ymin'])")
            exec(f"e.SubElement(bndbox_{i},'xmax').text = str(z['bndbox']['xmax'])")
            exec(f"e.SubElement(bndbox_{i},'ymax').text = str(z['bndbox']['ymax'])")
#                 else:
#                     pass
#             else:
#                 pass
    else:
        i =0
        z = jason['annotation']['object']
#         if (((z['bndbox']['xmax']) <= shape[1])&((z['bndbox']['ymax']) <= shape[0])):
#             if (((z['bndbox']['xmax']) >= 0)&((z['bndbox']['ymax']) >= 0)&((z['bndbox']['xmin']) >= 0)&((z['bndbox']['ymin']) >= 0)):
        exec(f'object_{i}= e.SubElement(r,"object")') 
        exec(f'e.SubElement(object_{i},"name").text = str(z["name"])')
        exec(f'e.SubElement(object_{i},"pose").text = str(z["pose"])')
        exec(f'e.SubElement(object_{i},"truncated").text = str(z["truncated"])')
        exec(f'e.SubElement(object_{i},"difficult").text = str(z["difficult"])')
        exec(f'bndbox_{i} = e.SubElement(object_{i},"bndbox")')
        exec(f"e.SubElement(bndbox_{i},'xmin').text = str(z['bndbox']['xmin'])")
        exec(f"e.SubElement(bndbox_{i},'ymin').text = str(z['bndbox']['ymin'])")
        exec(f"e.SubElement(bndbox_{i},'xmax').text = str(z['bndbox']['xmax'])")
        exec(f"e.SubElement(bndbox_{i},'ymax').text = str(z['bndbox']['ymax'])")
#             else:
#                 pass
#         else:
#             pass
    a = e.ElementTree(r)
    a.write(os.path.join(dest_path,xml_name))


def mosaic_augmentation(source_dir,dest_path):
    # source_dir = "/home/tbal/lincode/modeling/gorad/yolov5/annotations/train_aug/"
    print(glob.glob(os.path.join(source_dir,"*.xml")))
    xml_file = sorted(glob.glob(os.path.join(source_dir,"*.xml")))
    random.shuffle(xml_file)
    random.shuffle(xml_file)
    xml_stack =  []
    image_stack = []
    jason_stack = []
    print(len(xml_file))
    for e,i in enumerate(range(0,len(xml_file)-4,4)):
        xml_stack =  []
        image_stack = []
        jason_stack = []
        for ii in range(4):
            print(i+ii)
            xml = xml_file[i+ii]
            xml_stack.append(xml)
            image_name = xml.replace("xml","jpg")
            img = cv2.imread(image_name)
            image_stack.append(img)
            jason = read_xml2json(xml)
            jason_stack.append(jason)
            # print(xml , image_name)

        #mosaic_images
        im0 = image_stack[0]
        im1 = image_stack[1]
        im2 = image_stack[2]
        im3 = image_stack[3]

        im_h1 = cv2.hconcat([im0, im1])
        im_h2 = cv2.hconcat([im2, im3])
        mosaic_image = cv2.vconcat([im_h1, im_h2])

        h = im3.shape[0]
        w = im3.shape[1]


        #mosaic annotations
        #top right
        # print("TOP RIGHT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        j1 = jason_stack[1]
        # print((type(j1["annotation"]["object"]) == dict))
        if (type(j1["annotation"]["object"]) == dict) :
            for b in j1["annotation"]["object"]["bndbox"]:
                # print(j1["annotation"]["object"]["bndbox"][b],"HERE")
                if b == "xmin" or b == "xmax":
                    # print(b)
                    j1["annotation"]["object"]["bndbox"][b] = str(int(j1["annotation"]["object"]["bndbox"][b]) + w)
                    # print("AFTER", j1["annotation"]["object"]["bndbox"][b])
                else:
                    # print(b)
                    pass
        elif (type(j1["annotation"]["object"]) == list):
            for bn in range(len(j1["annotation"]["object"])):
                for b in j1["annotation"]["object"][bn]["bndbox"]:
                    # print(j1["annotation"]["object"][bn]["bndbox"][b],"HERE")
                    if b == "xmin" or b == "xmax":
                        # print(b)
                        j1["annotation"]["object"][bn]["bndbox"][b] = str(int(j1["annotation"]["object"][bn]["bndbox"][b]) + w)
                        # print("AFTER", j1["annotation"]["object"][bn]["bndbox"][b])
                    else:
                        # print(b)
                        pass
        jason_stack[1] = j1

        #mosaic annotations
        #bottom left
        # print("BOTTOM LEFT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        j2 = jason_stack[2]
        # print((type(j2["annotation"]["object"]) == dict))
        if (type(j2["annotation"]["object"]) == dict) :
            for b in j2["annotation"]["object"]["bndbox"]:
                # print(j2["annotation"]["object"]["bndbox"][b],"HERE")
                if b == "ymin" or b == "ymax":
                    # print(b)
                    j2["annotation"]["object"]["bndbox"][b] = str(int(j2["annotation"]["object"]["bndbox"][b]) + h)
                    # print("AFTER", j2["annotation"]["object"]["bndbox"][b])
                else:
                    # print(b)
                    pass
        elif (type(j2["annotation"]["object"]) == list):
            for bn in range(len(j2["annotation"]["object"])):
                for b in j2["annotation"]["object"][bn]["bndbox"]:
                    # print(j2["annotation"]["object"][bn]["bndbox"][b],"HERE")
                    if b == "ymin" or b == "ymax":
                        # print(b)
                        j2["annotation"]["object"][bn]["bndbox"][b] = str(int(j2["annotation"]["object"][bn]["bndbox"][b]) + h)
                        # print("AFTER", j2["annotation"]["object"][bn]["bndbox"][b])
                    else:
                        # print(b)
                        pass
        jason_stack[2] = j2

        #mosaic annotations
        #bottom right
        # print("BOTTOM RIGHT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        j3 = jason_stack[3]
        # print((type(j3["annotation"]["object"]) == dict))
        if (type(j3["annotation"]["object"]) == dict) :
            for b in j3["annotation"]["object"]["bndbox"]:
                # print(j3["annotation"]["object"]["bndbox"][b],"HERE")
                if b == "xmin" or b == "xmax":
                    # print(b)
                    j3["annotation"]["object"]["bndbox"][b] = str(int(j3["annotation"]["object"]["bndbox"][b]) + w)
                    # print("AFTER", j3["annotation"]["object"]["bndbox"][b])
                elif b == "ymin" or b == "ymax":
                    # print(b)
                    j3["annotation"]["object"]["bndbox"][b] = str(int(j3["annotation"]["object"]["bndbox"][b]) + h)
                    # print("AFTER", j3["annotation"]["object"]["bndbox"][b])
                else:
                    # print(b)
                    pass
        elif (type(j3["annotation"]["object"]) == list):
            for bn in range(len(j3["annotation"]["object"])):
                # print(j3["annotation"]["object"][bn]["bndbox"])
                for b in j3["annotation"]["object"][bn]["bndbox"]:
                    # print(j3["annotation"]["object"][bn]["bndbox"][b],"HERE")
                    # print(b)
                    if b == "xmin" or b == "xmax":
                        # print(b)
                        j3["annotation"]["object"][bn]["bndbox"][b] = str(int(j3["annotation"]["object"][bn]["bndbox"][b]) + w)
                        # print("AFTER", j3["annotation"]["object"][bn]["bndbox"][b])
                    elif b == "ymin" or b == "ymax":
                        # print(b)
                        j3["annotation"]["object"][bn]["bndbox"][b] = str(int(j3["annotation"]["object"][bn]["bndbox"][b]) + h)
                        # print("AFTER", j3["annotation"]["object"][bn]["bndbox"][b])
                    else:
                        # print(b,"ELSE")
                        pass
        jason_stack[3] = j3


        # print("TOP LEFT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        jason_0 = jason_stack[0]
        if (type(jason_0["annotation"]["object"]) == dict):
            jason_0["annotation"]["object"] = [jason_0["annotation"]["object"]]
        #     print((type(jason_0["annotation"]["object"]) == dict))
        # print("TOP RIGHT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        jason_1= jason_stack[1]
        if (type(jason_1["annotation"]["object"]) == dict):
            jason_1["annotation"]["object"] = [jason_1["annotation"]["object"]]
        #     print((type(jason_1["annotation"]["object"]) == dict))
        # print("BOTTOM LEFT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        jason_2 = jason_stack[2]
        if (type(jason_2["annotation"]["object"]) == dict):
            jason_2["annotation"]["object"] = [jason_2["annotation"]["object"]]
        # print("BOTTOM RIGHT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        jason_3 = jason_stack[3]
        if (type(jason_3["annotation"]["object"]) == dict):
            jason_3["annotation"]["object"] = [jason_3["annotation"]["object"]]
            
        # print(len(jason_0["annotation"]["object"]))
        jason_0["annotation"]["object"].extend(jason_1["annotation"]["object"])
        # print(len(jason_0["annotation"]["object"]))
        jason_0["annotation"]["object"].extend(jason_2["annotation"]["object"])
        # print(len(jason_0["annotation"]["object"]))
        jason_0["annotation"]["object"].extend(jason_3["annotation"]["object"])
        # print(len(jason_0["annotation"]["object"]))

        shape = mosaic_image.shape
        # print(jason_0)
        # print(jason_0["annotation"]["filename"])
        # jason_0["filename"] = str(e)+"_"+jason_0["annotation"]["filename"]+"_"+jason_1["annotation"]["filename"]+"_"+jason_2["annotation"]["filename"]+jason_3["annotation"]["filename"]
        jason_0["annotation"]["filename"] = str(e)+"_"+str(uuid.uuid1())+".jpg"
        jason_0["annotation"]["filename"] = jason_0["annotation"]["filename"].replace(".jpg","")
        jason_0["annotation"]["filename"] = jason_0["annotation"]["filename"]+".jpg"
        jason_0["annotation"]["path"] = dest_path
        image_name = os.path.join(dest_path,jason_0["annotation"]["filename"])
        xml_name = jason_0["annotation"]["filename"].replace(".jpg",".xml")
        print(image_name,xml_name)
        jason = jason_0
        # try:
        write_xml(jason,xml_name,dest_path,shape)
        
        cv2.imwrite(image_name,mosaic_image)
        # except Exception as e:
        #     print(e)
        #     pass



if __name__ == "__main__":
    source_dir = "D:\\lincode\\magna\\ATV\\training_data\\batch_9\\"
    dest_path = "D:\\lincode\\magna\\ATV\\training_data\\batch_9_mosaic\\"
    create_directory(dest_path)
    mosaic_augmentation(source_dir,dest_path)

