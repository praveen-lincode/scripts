import glob
import os 
import xml.etree.ElementTree as ET
# import cv2
import random
import shutil
from all_classes import *
# import all_classes

# classes = macro_classes

def check_for_class(file, classes):
    tree = ET.parse(file)   
    for elt in tree.iter():
        if ((elt.tag == 'name') & ((elt.text in classes))):
            return True
    return False

def create_folder(out = "val"):
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    print(out , ' created!')

def copy_images_xml_val(folder, num ,dest_dir = "val"):
    # create_folder(dest_dir)
    file_list = glob.glob(os.path.join(folder , "*.xml"))
    random.shuffle(file_list)
    random.shuffle(file_list)
    for i in range(num):
        try:
            # xml_file = random.choice(file_list)
            xml_file = file_list[i]
            img_file = xml_file.replace("xml","jpg") 
            shutil.move(xml_file, dest_dir)
            shutil.move(img_file, dest_dir)
        except Exception as e:
            print(e)
            pass


def copy_images_xml_train(folder, dest_dir = "train"):
    # create_folder(dest_dir)
    file_list = glob.glob(os.path.join(folder , "*.xml"))
    for xml_file in file_list:
        # xml_file = random.choice(file_list)
        try:
            # copy_file = check_for_class(xml_file, classes)
            # if copy_file:
            img_file = xml_file.replace("xml","jpg") 
            shutil.copy(xml_file, dest_dir)
            shutil.copy(img_file, dest_dir)
        except Exception as e:
            print(e)
            pass

# classes = ["batch_1","batch_2"
#           ]

def main():
    create_folder(out = "train")
    create_folder(out = "train_1")
    create_folder(out = "val")
    for b in range(200):
        c_n = f"batch_{b}"
        print(c_n)
    # for c_n in classes:
        copy_images_xml_train(folder= c_n, dest_dir = "train")
    # copy_images_xml_val(folder = "train" , num = 7500 ,dest_dir = "train_1")
    # copy_images_xml_val(folder = "train" , num = 1000 ,dest_dir = "val")
if __name__ == '__main__':
    main()
