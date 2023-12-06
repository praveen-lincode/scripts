## python script to change image name and corresponding xml name in a sequential order
# python change_imageandxmlnames_tagnames.py <folder-path-where-all-files-stored> <name-prefix>
# python change_imageandxmlnames_tagnames.py <G:\\Shriram_pistons\\ANNOTATIONS\\Piston> <Dent-scratch>
#cleaned code of enumerate6.py

import os
import sys
import glob
import xml.etree.ElementTree as ET

def changefilenameinxml(directory,dst_xmllist):
    files = dst_xmllist

    for file in files:
        filewithpath =  os.path.join(directory,file)
        tree = ET.parse(filewithpath)
        root = tree.getroot()
        filename = root.find('filename')
        root.find('filename').text = file.split(".")[0] + '.jpg' #rewrite the name of the tag with the xmlname
        tree.write(filewithpath)
    print("Successfully changed the filename tag inside the xmls...")
    return

def changepathnameinxml(directory,dst_xmllist,dst_imglist):
    files = dst_xmllist
    filesms = dst_imglist

    for file,filem in zip(files,filesms):
        filewithpath =  os.path.join(directory,file)
        tree = ET.parse(filewithpath)
        root = tree.getroot()
        filename = root.find('path')
        root.find('path').text = os.path.join(directory,filem) #rewrite the name of the tag with the xmlname
        tree.write(filewithpath)
    print("Successfully changed the 'path' tag inside the xmls...")
    return

directory = sys.argv[1]
name_prefix = sys.argv[2]

file_list = os.listdir(directory)

image_list = [f for f in os.listdir(directory) if f.endswith('.jpg')]
xml_list = [f for f in os.listdir(directory) if f.endswith('.xml')]


if len(image_list) == len(xml_list):
    i = 1
    src_imglist = []
    src_xmllist = []
    dst_imglist = []
    dst_xmllist = []
    for image, xml in zip(image_list, xml_list):
        src = directory + '/' + str(image)
        dst = directory + '/' + name_prefix  + str(i) + '.jpg'
        src_imglist.append(image)
        dst_imglist.append(name_prefix  + str(i) + '.jpg')
        os.rename(src, dst)
        src1 = directory + '/' + xml
        dst1 = directory + '/' + name_prefix  + str(i) + '.xml'
        src_xmllist.append(xml)
        dst_xmllist.append(name_prefix  + str(i) + '.xml')
        os.rename(src1, dst1)
        i += 1
print("Successfully changed the image and xml names with the prefix...")
changefilenameinxml(directory,dst_xmllist)
changepathnameinxml(directory,dst_xmllist,dst_imglist)