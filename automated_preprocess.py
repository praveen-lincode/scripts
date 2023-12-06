import glob
import shutil
import os
import cv2
import argparse
import sys
from transformer import Transformer
import logging
import threading
import time
from xml_json_xml import *
import imagesize



# stage = '17'

root_dir = "/home/tbal/lincode/modeling/gorad/"
yolo_dir = os.path.join(root_dir,'yolov5')
project_name = "tbal"
valid_dir = 'val_aug'
data_dir = os.path.join(yolo_dir,'data')
project_dir  = os.path.join(data_dir ,project_name)
train_img_dest_dir = os.path.join(project_dir,'images/train')
train_lbl_dest_dir = os.path.join(project_dir,'labels/train')
val_img_dest_dir = os.path.join(project_dir,'images/val')
val_lbl_dest_dir = os.path.join(project_dir,'labels/val')
temp_dir = os.path.join(yolo_dir,'XmlToTxt/xml')
txt_dir  = os.path.join(yolo_dir,'XmlToTxt/out')
annotation_folder = os.path.join(yolo_dir,'annotations')
train_xml = './train_xml'
train_xml_edited = './train_xml_edited'
train_out = './train_out'
val_xml = './val_xml'
val_xml_edited = './val_xml_edited'
val_out   = './val_out'
 
batches = ["train_aug"#,"train_3",
            #"train_aug_aug","train_1_aug","train_2_aug","train_3_aug"
       ]
def create_folder(out):
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    print(out , ' created!')


def copy_txt(text_file,dest_dir):
    shutil.copy(text_file, dest_dir)
    print(text_file +' is copied to '+ dest_dir+'!')

def read_txt(dest_dir):
    f = open("classes.txt", "r")
    shutil.copy("classes.txt", dest_dir)
    # os.rename(dest_dir+'/'','career.guru99.txt') 

def copy_files(source_dir,dest_dir):
    create_folder(dest_dir)
    for root, dirs, files in os.walk(source_dir, topdown=False):
        for filename in glob.glob((os.path.join(root,str([d for d in dirs]), '*.*'))):
            shutil.copy(filename, dest_dir)

def copy_xmls(source_dir,dest_dir):
    create_folder(dest_dir)
    for root, dirs, files in os.walk(source_dir, topdown=False):
        # print(root,dirs)
        # for i in files :
        #     if i.endswith('.xml'):
        #         print(i)
        #         shutil.copy(i, dest_dir)
        if dirs ==[]:
            for filename in glob.glob(os.path.join(source_dir , '*.xml')):
                # print(filename)
                shutil.copy(filename, dest_dir)
        else:   
            for filename in glob.glob((os.path.join(root,str([d for d in dirs]),'*.xml'))):
                shutil.copy(filename, dest_dir)
    print('XML copying done!')

def copy_images(source_dir,dest_dir):
    create_folder(dest_dir)
    types = ('/*.jpg', '/*.png')
    for t in types:
        for root, dirs, files in os.walk(source_dir, topdown=False):
            if dirs ==[]:
                for filename in glob.glob(root +t):
                    shutil.copy(filename, dest_dir)
            else:   
                for filename in glob.glob((os.path.join(root,str([d for d in dirs]),t))):
                    shutil.copy(filename, dest_dir)
    print('Images copying done!')


def copy_txts(source_dir,dest_dir):
    create_folder(dest_dir)
    for root, dirs, files in os.walk(source_dir, topdown=False):
        if dirs ==[]:
            for filename in glob.glob(root + '/*.txt'):
                shutil.copy(filename, dest_dir)
        else:   
            for filename in glob.glob((os.path.join(root,str([d for d in dirs]), '*.*'))):
                shutil.copy(filename, dest_dir)
    print('TXT copying done!')



def copy_batches(source_dir,dest_dir,extensions,data_type):
    create_folder(dest_dir)
    for b in batches:
        print(annotation_folder+'/'+b)
        # print(list(os.walk(annotation_folder+'/'+b, topdown=False)))
        for root, dirs, files in os.walk(annotation_folder+'/'+b, topdown=False):
            # print("here::::::::::",root, dirs, files)
            if dirs ==[]:
                # print("here::::::::::",root, dirs, files)
                for t in extensions:
                    for filename in glob.glob(root +'/*'+ t):
                        # print(filename)
                        shutil.copy(filename, dest_dir)
            else: 
                # print("here::::::::::",root, dirs, files)
                for t in extensions:  
                    for filename in glob.glob((os.path.join(root,str([d for d in dirs]),'/*', t))):
                        # print(filename)
                        shutil.copy(filename, dest_dir)

    print(data_type ,' batches copying done!')

def copy_batches_images(source_dir,dest_dir):
    create_folder(dest_dir)
    types = ('/*.jpg', '/*.png')
    for b in batches:
        for root, dirs, files in os.walk(annotation_folder+'/'+b, topdown=False):
            if dirs ==[]:
                for t in types:
                    for filename in glob.glob(root+'/' + t):
                        shutil.copy(filename, dest_dir)
            else: 
                for t in types:  
                    for filename in glob.glob((os.path.join(root,str([d for d in dirs]), t))):
                        shutil.copy(filename, dest_dir)
    print('images batches copying done!')

def copy_batches_xmls(source_dir,dest_dir):
    create_folder(dest_dir)
    for b in batches:
        for root, dirs, files in os.walk(annotation_folder+'/'+b, topdown=False):
            if dirs ==[]:
                for filename in glob.glob(root + '/*.xml'):
                    shutil.copy(filename, dest_dir)
            else:   
                for filename in glob.glob((os.path.join(root,str([d for d in dirs]), '*.xml'))):
                    shutil.copy(filename, dest_dir)
    print('xml batches copying done!')

def xml2txt(xml_dir,out_dir):
    create_folder(out_dir)
    parser = argparse.ArgumentParser(description="Formatter from ImageNet xml to Darknet text format")
    parser.add_argument("-xml", help="Relative location of xml files directory", default = 'xml')
    parser.add_argument("-out", help="Relative location of output txt files directory", default="out")
    args = parser.parse_args()

    xml_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), xml_dir)
    if not os.path.exists(xml_dir):
        print("Provide the correct folder for xml files.")
        sys.exit()

    out_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.access(out_dir, os.W_OK):
        print("%s folder is not writeable.")
        sys.exit()

    transformer = Transformer(xml_dir=xml_dir, out_dir=out_dir)
    transformer.transform()

    print('XML to TXT convertion done!')



def same_seed_random():
    np.random.seed(42)
    print(np.random.random())



def check_files(img_folder,lbl_folder):
    txt = []
    img = []

    for file in glob.glob(lbl_folder + '/*.*'):
        txt.append((file.split('/')[-1]).split('.')[0])
        
    for file in glob.glob(img_folder + '/*.*'):
        img.append((file.split('/')[-1]).split('.')[0])
    txt.sort();img.sort()

    c_i = 0
    for i in img:
        if i not in txt:
            print(i ,' txt file missing')
            c_i +=1
    print(c_i)
    print('Files checking done!')
    c_t = 0
    for i in txt:
        if i not in img:
            print(i ,' imgfile missing')
            c_t +=1
    print(c_t)
    print('Files checking done!')
    print('No of files missing :',c_i - c_t)



def create_traintxt(path,dest_folder):
    s = []
    for file in sorted(glob.glob(path + '/*.*')):
    #     print(file)
        s.append(file)
    file1 = open(dest_folder + "/train.txt","w")
    [file1.writelines(file + '\n') for file in s]  
    file1.close()

    print('Train.txt created!')

def create_valtxt(path,dest_folder):
    s = []
    for file in sorted(glob.glob(path + '/*.*')):
    #     print(file)
        s.append(file)
    file1 = open(dest_folder + "/val.txt","w")
    [file1.writelines(file + '\n') for file in s]  
    file1.close()
    print('val.txt created!')

def create_train_shape_txt(path,dest_folder):
    s = []
    for file in sorted(glob.glob(path + '/*.*')):
        try:
        #     file = cv2.imread(file)
        # #     print(file.shape[1],file.shape[0])
        #     a  = str(file.shape[1])+ ' ' + str(file.shape[0])
            width, height = imagesize.get(file)
            a  = str(height)+ ' ' + str(width)
            s.append(a)
        except Exception as e:
            print(e)
            print(file)
            pass
    file1 = open(dest_folder + "/train.shapes","w")
    [file1.writelines(file + '\n') for file in s]  
    file1.close()
    print('Train.shapes created!')

def create_val_shape_txt(path,dest_folder):
    s = []
    for file in sorted(glob.glob(path + '/*.*')):
    #     file = cv2.imread(file)
    # #     print(file.shape[1],file.shape[0])
    #     a  = str(file.shape[1])+ ' ' + str(file.shape[0])
        width, height = imagesize.get(file)
        a  = str(height)+ ' ' + str(width)
        s.append(a)
    file1 = open(dest_folder + "/val.shapes","w")
    [file1.writelines(file + '\n') for file in s]  
    file1.close()
    print('val.shapes created!')

def create_cataler_data_txt(dest_folder,subfolder):
    # f = open("classes.txt", "r")
    # file1 = open(dest_folder +"/cataler.names",'w')
    # file1.write(f.read())
    # file1.close()
    f = open("classes.txt", "r")
    lis = f.read().split('\n')
    if "" in lis:
        lis.remove("")
    try:
        lis.remove("")
    except:
        pass
    print('classes:',lis)
    classes = str('classes='+str(len(lis)))
    nc = str('nc : '+str(len(lis)))
    train = f'train : {subfolder}/train.txt'
    val = f'val : {subfolder}/val.txt'
    # names = f'names : data/{project_name}.names'
    names = f'names : {lis}'

    #####
    # file2 = open(dest_folder +"/cataler.data","w")
    # file2.write(classes + '\n'+train +'\n'+val+'\n'+names)
    # file2.close()
    # print('cataler.data created!')
    ####
    # file2 = open(os.path.join(dest_folder ,(project_name+".yaml"),"w"))
    file2 = open(f'{dest_folder}/{project_name}.yaml',"w")
    file2.write(nc + '\n'+train +'\n'+val+'\n'+names)
    file2.close()
    print(f'{project_name}.yaml created!')


def get_classes():
    f = open("classes.txt", "r")
    classes = (f.read()).split('\n')
    return classes

def create_train_data():
    # ''''# copy_batches_images(annotation_folder,train_img_dest_dir)
    # # copy_batches_xmls(annotation_folder,train_xml)''''
    copy_batches(annotation_folder,train_img_dest_dir,['.jpg','.png','.JPG','.PNG'],'Images')
    copy_batches(annotation_folder,train_xml,['.xml'],'XMLS')
    classes = get_classes()
    edit_xmls(train_xml,train_xml_edited)
    xml2txt(train_xml_edited,train_out)
    copy_txts(train_out,train_lbl_dest_dir )
    check_files(train_img_dest_dir,train_lbl_dest_dir)    
    create_traintxt(train_img_dest_dir,project_dir)
    create_train_shape_txt(train_img_dest_dir,project_dir)
    print('Training dataset created')

def create_val_data():
    copy_images(os.path.join(annotation_folder, valid_dir),val_img_dest_dir)
    copy_xmls(os.path.join(annotation_folder, valid_dir),val_xml)
    #    copy_batches(os.path.join(annotation_folder, valid_dir),val_img_dest_dir,['.jpg','.png','.JPG','.PNG'],'Images')
    #copy_batches(os.path.join(annotation_folder, valid_dir),val_xml,['.xml'],'XMLS')
    # classes = get_classes()
    edit_xmls(val_xml,val_xml_edited)
    xml2txt(val_xml_edited,val_out)
    copy_txts(val_out,val_lbl_dest_dir )
    check_files(val_img_dest_dir,val_lbl_dest_dir)
    create_valtxt(val_img_dest_dir,project_dir)
    create_val_shape_txt(val_img_dest_dir,project_dir)

    print('validation dataset created')

if __name__ == "__main__":
    create_train_data()
    create_val_data()
    create_cataler_data_txt(data_dir,project_dir)

    # t1 = threading.Thread(target=create_train_data()) 
    # t2 = threading.Thread(target=create_val_data()) 

    # starting thread 1 
    # t1.start() 
    # starting thread 2 
    # t2.start() 
    # wait until thread 1 is completely executed 
    # t1.join() 
    # wait until thread 2 is completely executed 
    # t2.join() 

    # create_cataler_data_txt(data_dir,project_dir)
  
    # both threads completely executed 
    print("Done!") 



