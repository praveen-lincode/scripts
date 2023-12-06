import glob
import imageio
import imgaug as ia
import imgaug.augmenters as iaa
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
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import sys
import time
import threading
from multiprocessing import Process

# source_path = '/home/lincode/Indo_medical/training/yolov3/yolov3/annotations/batch_16'
# dest_path = source_path +"_aug/"

augment_list = ["drop","rotate_90","contrast","flip_vr"]#'rotate','flip_hr','flip_vr',,'resize''crop',
#'crop','flip_hr','flip_vr','crop','brightness','flip_hr','flip_vr',,'contrast','brightness',

##Augmentations

#crop
CropAndPad             = iaa.CropAndPad(px=(6000, 0))
Crop                   = iaa.Crop(px  =(6000, 4000))
crop_fixed_center      = iaa.CenterCropToFixedSize(height=4500, width=0)#height=200, width=440#height=450, width=750)
CropToSquare           = iaa.CropToSquare()
Pad                    = iaa.Pad(px=(0, 10))
CenterPadToFixedSize   = iaa.CenterPadToFixedSize(height=20, width=30)
CropToAspectRatio      = iaa.CropToAspectRatio(2.0)
CenterCropToFixedSize  = iaa.CenterCropToFixedSize(height=0, width=6000)
CenterCropToMultiplesOf= iaa.CenterCropToMultiplesOf(height_multiple=10, width_multiple=6)
PadToAspectRatio       = iaa.PadToAspectRatio(2.0)
CropToFixedSize        = iaa.CropToFixedSize(width=6000, height=4500,position="left-top")
CropToPowersOf         = iaa.CropToPowersOf(height_base=3, width_base=2)
CropToMultiplesOf      = iaa.CropToMultiplesOf(height_multiple=4500, width_multiple=6000)

# {‘uniform’, ‘normal’, ‘center’, ‘left-top’, ‘left-center’,
#  ‘left-bottom’, ‘center-top’, ‘center-center’, ‘center-bottom’, 
# ‘right-top’, ‘right-center’, ‘right-bottom’} 

CropToFixedSize_uniform      = iaa.CropToFixedSize(width=6000, height=4500,position="uniform")
CropToFixedSize_normal      = iaa.CropToFixedSize(width=6000, height=4500,position="normal")
CropToFixedSize_center      = iaa.CropToFixedSize(width=6000, height=4500,position="center")
CropToFixedSize_left_top     = iaa.CropToFixedSize(width=6000, height=4500,position="left-top")
CropToFixedSize_left_bottom     = iaa.CropToFixedSize(width=6000, height=4500,position="left-bottom")
CropToFixedSize_center_top     = iaa.CropToFixedSize(width=6000, height=4500,position="center-top")
CropToFixedSize_center_center      = iaa.CropToFixedSize(width=6000, height=4500,position="center-center")
CropToFixedSize_center_bottom     = iaa.CropToFixedSize(width=6000, height=4500,position="center-bottom")
CropToFixedSize_right_top      = iaa.CropToFixedSize(width=6000, height=4500,position="right-top")
CropToFixedSize_right_center      = iaa.CropToFixedSize(width=6000, height=4500,position="right-center")
CropToFixedSize_right_bottom     = iaa.CropToFixedSize(width=6000, height=4500,position="right-bottom")

augmentations = {"CropAndPad":CropAndPad,
                "CenterPadToFixedSize":CenterPadToFixedSize,
                "Crop":Crop,
                "CropToSquare":CropToSquare,
                "Pad":Pad,
                "CropToAspectRatio":CropToAspectRatio,
                "CenterCropToFixedSize":CenterCropToFixedSize,
                "CenterCropToMultiplesOf":CenterCropToMultiplesOf,
                "PadToAspectRatio":PadToAspectRatio,
                "CropToFixedSize":CropToFixedSize,
                "CropToPowersOf":CropToPowersOf,
                "CropToMultiplesOf":CropToMultiplesOf
                }

augmentations = {
    "CropToFixedSize_uniform":CropToFixedSize_uniform ,
    "CropToFixedSize_normal":CropToFixedSize_normal,
    "CropToFixedSize_center":CropToFixedSize_center ,
    "CropToFixedSize_left_top" :  CropToFixedSize_left_top,
    "CropToFixedSize_left_bottom":  CropToFixedSize_left_bottom,
    "CropToFixedSize_center_top" : CropToFixedSize_center_top,
    "CropToFixedSize_center_center" :CropToFixedSize_center_center,
    "CropToFixedSize_center_bottom" :CropToFixedSize_center_bottom,
    "CropToFixedSize_right_top"  :CropToFixedSize_right_top,
    "CropToFixedSize_right_center"   :CropToFixedSize_right_center,
    "CropToFixedSize_right_bottom"  :CropToFixedSize_right_bottom}
def create_directory(directory):#create directory
    try:
        os.makedirs(directory)
    except:
        print('directory already exists!!')

def del_create_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)  # delete output folder
        print(directory ,' already exists!!')
        print(directory ,'Removed')
        os.makedirs(directory)
    else:
        os.makedirs(directory) # make new output folder
    print(directory , ' created!')

def read_xml2json(file):
    with open(file) as xml_file:
        my_dict=xmltodict.parse(xml_file.read())
    xml_file.close()
    json_data=json.dumps(my_dict)
    jason = json.loads(json_data)
    # print(file ,'converted to json!')
    return jason

def read_image(jason,source_path):
    img_file = jason['annotation']['filename']
    image = imageio.imread(source_path+'/'+img_file)
    # print(img_file ,' Image found!!')
    return image

def unique_id():
    id = uuid.uuid4() 
    return id

def uid_rename_file(jason):
    id = unique_id()
    img_file = jason['annotation']['filename']
    img_name = img_file.replace(img_file[-4],str(id)+img_file[-4])
    xml_name = img_name.replace(img_name[-4:],'.xml')
    return img_name,xml_name

def aug_rename_file(jason,aug):
    id = str(aug)
    img_file = jason['annotation']['filename']
    img_name = img_file.replace(img_file[-4],"_"+str(id)+img_file[-4])
    xml_name = img_name.replace(img_name[-4:],'.xml')
    return img_name,xml_name

def objects_coord_aug(jason,augment,image):#json format and which augumantation and image
    object_list = []
    # print(type(jason['annotation']['object']))
    # print(len(jason['annotation']['object']))
    # for i,x in enumerate(jason['annotation']['object']):
    object_dict = {'name': '',
    'pose': 'Unspecified',
    'truncated': '0',
    'difficult': '0',
    'bndbox': {}}
    x = jason['annotation']['object']
    x1,y1,x2,y2 = x['bndbox']['xmin'],x['bndbox']['ymin'],x['bndbox']['xmax'],x['bndbox']['ymax']
    bbs = BoundingBoxesOnImage([BoundingBox(x1=int(x1), x2=int(x2), y1=int(y1), y2=int(y2))], shape=image.shape)
    image_aug, bbs_aug = augment(image=image, bounding_boxes=(bbs))
    coordinates = bbs_aug.to_xyxy_array()
    xmin,ymin,xmax,ymax = (coordinates[0][0]),(coordinates[0][1]),(coordinates[0][2]),(coordinates[0][3])  
    print(xmin,ymin,xmax,ymax)
    object_dict['name']=x['name']
    object_dict['bndbox']= {'xmin':int(xmin),'ymin':int(ymin),'xmax':int(xmax),'ymax':int(ymax)} 
    object_list=(object_dict)
    # print(object_list)
    return object_list,image_aug,image_aug.shape

#augmentation of img and bnd_box
def multi_objects_coord_aug(jason,augment,image):
    bbs_list = []
    object_list = []
    # print(len(jason['annotation']['object']))
    for i,x in enumerate(jason['annotation']['object']):#read the boubding box from the json 
        # if x == "bndbox":
        # print("here::::::::::::::",x ,len(x))
        # print(len(x))
        
        # try:
        # print(x['bndbox'])
        x1,y1,x2,y2 = (int(float(x['bndbox']['xmin'])),
                        int(float(x['bndbox']['ymin'])),
                        int(float(x['bndbox']['xmax'])),
                        int(float(x['bndbox']['ymax'])))
        # except Exception as e:
        #     print(e)
        #     x1,y1,x2,y2 = None,None,None,None


        # print()
        bbs_list.append(BoundingBox(x1=int(x1), x2=int(x2), y1=int(y1), y2=int(y2),label = str(x['name'])))
        # print(bbs_list)
        bbs = BoundingBoxesOnImage(bbs_list,shape=image.shape)   
        image_aug, bbs_aug = augment(image=image, bounding_boxes=(bbs))#augments the image and bounding boxes
    for i,x in enumerate(jason['annotation']['object']):
        object_dict = {'name': '',
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': {}}
        # print(bbs_aug[i].x1_int)
        xmin,ymin,xmax,ymax = bbs_aug[i].x1_int,bbs_aug[i].y1_int,bbs_aug[i].x2_int,bbs_aug[i].y2_int
        print("Image Shape::",image_aug.shape)
        height,width,c = image_aug.shape
        print("Before modified:",xmin,ymin,xmax,ymax)
        # Box chop
        if xmin < 0:
            xmin = 0#;print("xmin Modified!!")
        if ymin < 0:
            ymin = 0#;print("ymin Modified!!")
        if xmax > width :
            xmax = width#;print("xmax Modified!!")
        if ymax > height:
            ymax = height#;print("ymax Modified!!")
        
        print("After modified :",xmin,ymin,xmax,ymax)
        if  xmax < 0 or ymax < 0 or xmin > width or ymin>height:
            print("Annotation out of bounds")
            # pass
        else:
            object_dict['name']=x['name']
            object_dict['bndbox']= {'xmin':int(xmin),'ymin':int(ymin),'xmax':int(xmax),'ymax':int(ymax)} 
            object_list.append(object_dict)
            # print(object_dict)
    # print(object_list)
        del xmin;del ymin;del xmax;del ymax 
    return object_list,image_aug ,image_aug.shape


def edit_jason(jason,object_list,aug,shape): #Edit the json
    img_name,xml_name = aug_rename_file(jason,aug)
    jason['annotation']['folder'] = str(dest_path.split('/')[-1])
    jason['annotation']['path'] = dest_path + img_name
    jason['annotation']['filename'] = img_name
    jason['annotation']['object'] = object_list
    jason['annotation']["size"]['width'] = shape[1]
    jason['annotation']["size"]['height'] = shape[0]
    jason['annotation']["size"]['depth'] = shape[2]
    return jason,img_name,xml_name

def write_xml(jason,xml_name,dest_path,shape): #converts json to xml and writes xml
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
    print('shape:',shape)
    if type(jason['annotation']['object']) == list:
        for i,z in enumerate(d['annotation']["object"]):
            # if (((z['bndbox']['xmax']) >= 0) & ((z['bndbox']['ymax']) >= 0)&((z['bndbox']['xmin']) >= 0)&((z['bndbox']['ymin']) >= 0)):
            if (((z['bndbox']['xmax']) <= shape[1])&((z['bndbox']['ymax']) <= shape[0])):
                if (((z['bndbox']['xmax']) >= 0)&((z['bndbox']['ymax']) >= 0)&((z['bndbox']['xmin']) >= 0)&((z['bndbox']['ymin']) >= 0)):
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
                    pass
            else:
                pass
    else:
        i =0
        z = jason['annotation']['object']
        if (((z['bndbox']['xmax']) <= shape[1])&((z['bndbox']['ymax']) <= shape[0])):
            if (((z['bndbox']['xmax']) >= 0)&((z['bndbox']['ymax']) >= 0)&((z['bndbox']['xmin']) >= 0)&((z['bndbox']['ymin']) >= 0)):
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
                pass
        else:
            pass
    a = e.ElementTree(r)
    a.write(dest_path+xml_name)

def write_image(dest_path,image_aug,img_name):
    imageio.imwrite(dest_path+img_name, image_aug)


def aug_img_bndbox( source_path,dest_path ,augment_list):
    del_create_directory(dest_path)
    for xml in sorted(glob.glob(source_path + '/*.xml')):
        start_time = time.time()
        jason = read_xml2json(xml)
        width = int(jason['annotation']["size"]['width'])
        height = int(jason['annotation']["size"]['height'])
        if height >= 6000 or width >= 6000:
            image = read_image(jason,source_path)
            CropToFixedSize_uniform      = iaa.CropToFixedSize(width=width//2, height=height//2,position="uniform")
            CropToFixedSize_normal       = iaa.CropToFixedSize(width=width//2, height=height//2,position="normal")
            CropToFixedSize_center       = iaa.CropToFixedSize(width=width//2, height=height//2,position="center")
            CropToFixedSize_left_top     = iaa.CropToFixedSize(width=width//2, height=height//2,position="left-top")
            CropToFixedSize_left_bottom  = iaa.CropToFixedSize(width=width//2, height=height//2,position="left-bottom")
            CropToFixedSize_center_top   = iaa.CropToFixedSize(width=width//2, height=height//2,position="center-top")
            CropToFixedSize_center_center= iaa.CropToFixedSize(width=width//2, height=height//2,position="center-center")
            CropToFixedSize_center_bottom= iaa.CropToFixedSize(width=width//2, height=height//2,position="center-bottom")
            CropToFixedSize_right_top    = iaa.CropToFixedSize(width=width//2, height=height//2,position="right-top")
            CropToFixedSize_right_center = iaa.CropToFixedSize(width=width//2, height=height//2,position="right-center")
            CropToFixedSize_right_bottom = iaa.CropToFixedSize(width=width//2, height=height//2,position="right-bottom")
            augmentations = {
                        "CropToFixedSize_uniform":CropToFixedSize_uniform ,
                        "CropToFixedSize_normal":CropToFixedSize_normal,
                        "CropToFixedSize_center":CropToFixedSize_center ,
                        "CropToFixedSize_left_top" :  CropToFixedSize_left_top,
                        "CropToFixedSize_left_bottom":  CropToFixedSize_left_bottom,
                        "CropToFixedSize_center_top" : CropToFixedSize_center_top,
                        "CropToFixedSize_center_center" :CropToFixedSize_center_center,
                        "CropToFixedSize_center_bottom" :CropToFixedSize_center_bottom,
                        "CropToFixedSize_right_top"  :CropToFixedSize_right_top,
                        "CropToFixedSize_right_center"   :CropToFixedSize_right_center,
                        "CropToFixedSize_right_bottom"  :CropToFixedSize_right_bottom}
            augment_list = [
                            # "CropToFixedSize_uniform" ,
                            # "CropToFixedSize_normal",
                            # "CropToFixedSize_center",
                            "CropToFixedSize_left_top",
                            "CropToFixedSize_left_bottom",
                            # "CropToFixedSize_center_top" ,
                            # "CropToFixedSize_center_center",
                            # "CropToFixedSize_center_bottom",
                            "CropToFixedSize_right_top",
                            # # "CropToFixedSize_right_center",
                            "CropToFixedSize_right_bottom"
                            ]

            for aug in augment_list:
                try:
                    jason = read_xml2json(xml)
                    # image = read_image(jason,source_path)
                    # image = image_orignal.copy()
                    augment = augmentations[aug]
                    try:
                        object_list,image_aug ,shape = multi_objects_coord_aug(jason,augment,image)                
                        # if type(jason['annotation']['object']) == dict:
                            # print('dict yes')
                    except:
                        # else:
                            # print('list yes')
                        object_list,image_aug ,shape= objects_coord_aug(jason,augment,image)
                    jason1,img_name,xml_name = edit_jason(jason,object_list,aug,shape)
                    write_xml(jason1,xml_name,dest_path,shape)
                    write_image(dest_path,image_aug,img_name)
                    print(xml , aug ,'augmented !')
                except Exception as e:
                    print(e)
                    pass
        end_time = time.time()
        time_elapsed = end_time - start_time
        print('Time taken augument per image', time_elapsed ,' secs')






if __name__ == "__main__":
    # from concurrent.futures import ThreadPoolExecutor
    start_time = time.time()
    source_path = f'/home/tbal/lincode/modeling/gorad/yolov5/annotations/train_aug'
    dest_path = source_path +"_aug/"

  
    augment_list = [
        "CropToFixedSize_uniform" ,

        ]

    aug_img_bndbox( source_path,dest_path ,augment_list)
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(start_time)
    print(end_time)
    print('Time elapsed ', time_elapsed ,' secs')


