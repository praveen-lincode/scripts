import glob
import os 
import xml.etree.ElementTree as ET
# import cv2
import random
import shutil
    
def create_folder(out = "val"):
    print(out)
    print(os.path.exists(out))
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    else:
        os.makedirs(out)  # make new output folder
        print(out , ' created!')

def copy_images_xml_val(folder, num ,dest_dir = "val"):
    # create_folder(out = dest_dir)
    file_list = glob.glob(os.path.join(folder , "*.xml"))
    random.shuffle(file_list)
    random.shuffle(file_list)
    for i in range(num):
        try:
            xml_file = file_list[i]
            img_file = xml_file.replace("xml","jpg") 
            shutil.move(xml_file, dest_dir)
            shutil.move(img_file, dest_dir)
        except Exception as e:
            print(e)
            pass


def copy_images_xml_train(folder, dest_dir = "train"):
    # create_folder(out = dest_dir)
    file_list = glob.glob(os.path.join(folder , "*.xml"))
    for xml_file in file_list:
        # xml_file = random.choice(file_list)
        try:
            img_file = xml_file.replace("xml","jpg") 
            shutil.copy(xml_file, dest_dir)
            shutil.copy(img_file, dest_dir)
        except Exception as e:
            print(e)
            pass
#
# classes = ["batch_1","batch_2"
#           ]

def main():

    # create_folder(out = "train_1")
    # create_folder(out = "train_2")
    # create_folder(out = "val")
    for b in range(200):
        c_n = f"batch_{b}"
        print(c_n)
    # for c_n in classes:
        copy_images_xml_train(folder= c_n, dest_dir = "train_1")
    c = int(len(os.listdir("train_1"))//10)
    # print(c)
    copy_images_xml_val(folder = "train_1" , num = 300 ,dest_dir = "val")
    # c = int(len(glob.glob(os.path.join("train_1" , "*.xml")))//2)
    # print(c)
    copy_images_xml_val(folder = "train_1" , num = 7500 ,dest_dir = "train_2")

if __name__ == '__main__':
    main()
