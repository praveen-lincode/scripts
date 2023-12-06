import glob
import os 
import xml.etree.ElementTree as ET
import cv2



count = 0

root_path = '/home/tbal/lincode/data_preparation/'

for i in range(18,23):
    path = f'/home/tbal/lincode/data_preparation/batch{i}'
    for file in glob.glob(os.path.join(path,'*.xml')):
    #     print((file.split('/')[-1]).split('.')[0])
        tree = ET.parse(file)
        for elt in tree.iter():
            if((elt.tag == 'name')) :#& (elt.text == 'black_mark')):
                count += 1
        tree.write(file)
        print(path)
print("TOTAL_COUNT:::::::",count)   
