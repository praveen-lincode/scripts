import glob
import os 
import xml.etree.ElementTree as ET
import cv2
import uuid

def create_directory(directory):#create directory
    try:
        os.makedirs(directory)
    except:
#         print('directory already exists!!')
        pass

import json as j
import xmltodict
import json
from xml.dom import minidom
import xml.etree.cElementTree as e
import glob
import numpy as np
import os
import glob
import shutil

import cv2
import argparse
import sys
import logging
import threading
import time
# from xml_json_xml import *

# src_path = '/home/gokul/Desktop/Cataler/data/RD'#/xmls'
# dest_path = '/home/gokul/Desktop/Cataler/data/RD'


def create_folder(out):
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    print(out , ' created!')


def read_xml2json(file):
    with open(file) as xml_file:
        my_dict=xmltodict.parse(xml_file.read())
    xml_file.close()
    json_data=json.dumps(my_dict)
    jason = json.loads(json_data)
    # print(file ,'converted to json!')
    return jason

def xml_object_edit(src_path,dest_path,classes):
    create_folder(dest_path)
    print('classes:',classes)
    for file in glob.glob(src_path+'/*.xml'):
        # print(file.split('/')[-1])
        with open(file) as xml_file:
            my_dict=xmltodict.parse(xml_file.read())
        xml_file.close()
        json_data=json.dumps(my_dict)
        d  = json.loads(json_data)
        jason = d
        r = e.Element("annotation")
        # e.SubElement('\n','\t')
        e.SubElement(r,"folder").text = d['annotation']["folder"]
        e.SubElement(r,"filename").text = d['annotation']["filename"]
        e.SubElement(r,"path").text = str(d['annotation']["path"])
        # e.SubElement(r,"source").text = str(d['annotation']["source"])
        source_ = e.SubElement(r,"source")
        e.SubElement(source_,'database').text = str(d['annotation']["source"]['database'])
        # e.SubElement(r,"size").text = str(d['annotation']["size"])
        size_ = e.SubElement(r,"size")
        # for s in d['annotation']["size"]:
        #     print(s)
        e.SubElement(size_,'width').text = str(d['annotation']["size"]['width'])
        e.SubElement(size_,'height').text = str(d['annotation']["size"]['height'])
        e.SubElement(size_,'depth').text = str(d['annotation']["size"]['depth'])


        e.SubElement(r,"segmented").text = str(d['annotation']["segmented"])
        # e.SubElement(r,"object").text = str(d['annotation']["object"])
        # object_ = e.SubElement(r,"object")
        # for i in range( len(d['annotation']["object"])):
        # for j,i in enumerate(range( len(d['annotation']["object"]))):
        removed = []
        # try:
        if type(jason['annotation']['object']) == list:
            for i,z in enumerate(d['annotation']["object"]):
                if z["name"] in classes:
                    exec(f'object_{i}= e.SubElement(r,"object")') 
                    exec(f'e.SubElement(object_{i},"name").text = str(z["name"])')
                    try:
                        exec(f'e.SubElement(object_{i},"pose").text = str(z["pose"])')
                    except:
                        exec(f'e.SubElement(object_{i},"pose").text = str(z["pos"])')
                    exec(f'e.SubElement(object_{i},"truncated").text = str(z["truncated"])')
                    exec(f'e.SubElement(object_{i},"difficult").text = str(z["difficult"])')
                    exec(f'bndbox_{i} = e.SubElement(object_{i},"bndbox")')
                    exec(f"e.SubElement(bndbox_{i},'xmin').text = str(z['bndbox']['xmin'])")
                    exec(f"e.SubElement(bndbox_{i},'ymin').text = str(z['bndbox']['ymin'])")
                    exec(f"e.SubElement(bndbox_{i},'xmax').text = str(z['bndbox']['xmax'])")
                    exec(f"e.SubElement(bndbox_{i},'ymax').text = str(z['bndbox']['ymax'])")
                else:
                    removed.append(z["name"])
        else:
            if z["name"] in classes:
                i =0
                z = jason['annotation']['object']
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
            else:
                removed.append(z["name"])

        # except:
        #     print('No Objects')

        a = e.ElementTree(r)
        a.write(dest_path + '/'+file.split('/')[-1])
    print('Removed classes',np.unique(removed))

def write_xml(jason,xml_name,dest_path,threshold): #converts json to xml and writes xml
    # print(jason)
    d = jason
    r = e.Element("annotation")
    e.SubElement(r,"folder").text = d['annotation']["folder"]
    e.SubElement(r,"filename").text = d['annotation']["filename"]
    e.SubElement(r,"path").text = str(d['annotation']["path"])
    source_ = e.SubElement(r,"source")
    e.SubElement(source_,'database').text = str(d['annotation']["source"]['database'])
    size_ = e.SubElement(r,"size")
    e.SubElement(size_,'width').text = str(d['annotation']["size"]['width'])
    e.SubElement(size_,'height').text = str(d['annotation']["size"]['height'])
    e.SubElement(size_,'depth').text = str(d['annotation']["size"]['depth'])


    e.SubElement(r,"segmented").text = str(d['annotation']["segmented"])

    w = int(d['annotation']["size"]['width'])
    h = int(d['annotation']["size"]['height'])

    
    if type(jason['annotation']['object']) == list:
        for i,z in enumerate(jason['annotation']["object"]):
            xmin = int(z['bndbox']['xmin'])
            ymin = int(z['bndbox']['ymin'])
            xmax = int(z['bndbox']['xmax'])
            ymax = int(z['bndbox']['ymax'])
            ok_box =  check_remove_boxes(threshold,w,h , xmin,xmax,ymin,ymax)
            if ok_box :#z["name"] in classes:
                # print('in list:',z["name"],classes)
                exec(f'object_{i}= e.SubElement(r,"object")') 
                exec(f'e.SubElement(object_{i},"name").text = str(z["name"])')
                try:
                    exec(f'e.SubElement(object_{i},"pose").text = str(z["pose"])')
                except:
                    exec(f'e.SubElement(object_{i},"pos").text = str(z["pos"])')
                exec(f'e.SubElement(object_{i},"truncated").text = str(z["truncated"])')
                exec(f'e.SubElement(object_{i},"difficult").text = str(z["difficult"])')
                exec(f'bndbox_{i} = e.SubElement(object_{i},"bndbox")')
                exec(f"e.SubElement(bndbox_{i},'xmin').text = str(z['bndbox']['xmin'])")
                exec(f"e.SubElement(bndbox_{i},'ymin').text = str(z['bndbox']['ymin'])")
                exec(f"e.SubElement(bndbox_{i},'xmax').text = str(z['bndbox']['xmax'])")
                exec(f"e.SubElement(bndbox_{i},'ymax').text = str(z['bndbox']['ymax'])")
            # else:
            #     print('Not in list:',z["name"])
    else:
        i =0
        z = jason['annotation']['object']
        # print('Not in list:',z["name"])
        xmin = int(z['bndbox']['xmin'])
        ymin = int(z['bndbox']['ymin'])
        xmax = int(z['bndbox']['xmax'])
        ymax = int(z['bndbox']['ymax'])
        ok_box =  check_remove_boxes(threshold,w,h , xmin,xmax,ymin,ymax)
        if ok_box :
        # if z["name"] in classes:
            exec(f'object_{i}= e.SubElement(r,"object")') 
            exec(f'e.SubElement(object_{i},"name").text = str(z["name"])')
            try:
                exec(f'e.SubElement(object_{i},"pose").text = str(z["pose"])')
            except:
                exec(f'e.SubElement(object_{i},"pos").text = str(z["pos"])')
            exec(f'e.SubElement(object_{i},"truncated").text = str(z["truncated"])')
            exec(f'e.SubElement(object_{i},"difficult").text = str(z["difficult"])')
            exec(f'bndbox_{i} = e.SubElement(object_{i},"bndbox")')
            exec(f"e.SubElement(bndbox_{i},'xmin').text = str(z['bndbox']['xmin'])")
            exec(f"e.SubElement(bndbox_{i},'ymin').text = str(z['bndbox']['ymin'])")
            exec(f"e.SubElement(bndbox_{i},'xmax').text = str(z['bndbox']['xmax'])")
            exec(f"e.SubElement(bndbox_{i},'ymax').text = str(z['bndbox']['ymax'])")
        # else:
        #     print(z["name"])
    a = e.ElementTree(r)
    a.write(os.path.join(dest_path,xml_name))
    # print()
def get_classes():
    f = open("classes.txt", "r")
    classes = (f.read()).split('\n')
    if "" in classes:
        classes.remove("")
    return classes




def chek_boxes():
    anno_path = '/home/tbal/lincode/modeling/gorad/yolov5/annotations/val_aug'
    padding = 0
    for batch in range(1):
        path = anno_path#os.path.join(anno_path,f'batch_{batch}')
        print(path)
        for file in glob.glob(os.path.join(path,'*.xml')):
            img_file = file.replace("xml","jpg")
            img = cv2.imread(img_file)
            print(img.shape)
            tree = ET.parse(file)
            root = tree.getroot()
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                # storage_dir = os.path.join(data_dir,class_name)
                # create_directory(directory = storage_dir)
                try:
                    try:
                        xmin = int(obj.find('bndbox//xmin').text) - padding
                        ymin = int(obj.find('bndbox//ymin').text) - padding
                        xmax = int(obj.find('bndbox//xmax').text) + padding
                        ymax = int(obj.find('bndbox//ymax').text) + padding
                        # img_name = str(uuid.uuid1())+ ".jpg"
                        # img_path = os.path.join(storage_dir,img_name)
    #                     print(img_file)
                        # cv2.imwrite(img_path,img[int(ymin):int(ymax),int(xmin):int(xmax)])
                    except Exception as e:
                        xmin = int(obj.find('bndbox//xmin').text)
                        ymin = int(obj.find('bndbox//ymin').text) 
                        xmax = int(obj.find('bndbox//xmax').text) 
                        ymax = int(obj.find('bndbox//ymax').text) 
                        # img_name = str(uuid.uuid1())+ ".jpg"
                        # img_path = os.path.join(storage_dir,img_name)
    #                     print(img_file)
                        # cv2.imwrite(img_path,img[int(ymin):int(ymax),int(xmin):int(xmax)])
                        print(e)
                        pass
                    x_pixels = xmax - xmin
                    y_pixels = ymax - ymin

                    box_area = x_pixels * y_pixels

                    print("x_pixels::::",x_pixels)
                    print("y_pixels::::",y_pixels)
                    print("box_area::::",box_area)
                
                except Exception as e:
                    print(e)
                    pass
                print("#############################################################################################")



def check_remove_boxes(threshold,w,h , xmin,xmax,ymin,ymax):
    x_pixels = xmax - xmin
    y_pixels = ymax - ymin
    box_area = x_pixels * y_pixels
    image_size  = w * h
    
    if  (box_area/image_size)*100 < threshold:
        print(box_area ,image_size )
        print((box_area/image_size)*100)
        return False
    else:
        return True

def edit_xmls(src_path,dest_path):
    classes = get_classes()
    # create_folder(dest_path)
    print(classes)
    for file in glob.glob(src_path+'/*.xml'):
        try:
            # print(file)
            jason = read_xml2json(file)
            xml_name = file.split('/')[-1]
            write_xml(jason,xml_name,dest_path,classes)
        except Exception as e:
            print(e)
            pass

def remove_boxes(source_dir ,dest_path,threshold):
    create_folder(dest_path)
    for xml_file in glob.glob(os.path.join(source_dir , "*.xml")):
        try:
            jason = read_xml2json(xml_file)
            xml_name = xml_file.split('/')[-1]
            write_xml(jason,xml_name,dest_path,threshold)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    source_dir = "/home/tbal/lincode/modeling/gorad/yolov5/annotations/val_aug"
    dest_path = "/home/tbal/lincode/modeling/gorad/yolov5/annotations/val_aug_1"
    threshold = 5
    remove_boxes(source_dir ,dest_path,threshold)