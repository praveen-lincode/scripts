import glob
import os 
import xml.etree.ElementTree as ET
import cv2
from all_classes import *


count = 0
not_change_count = 0

root_path = "D:\\lincode\\magna\\ATV\\training_data\\"
paths = ["label"]#,"train_1","train_2"]
remove_classes = remove_classes#["paint_feather_strip_residue","fastner_missing","sealant"]#,"electrical_tape"
rename_classes = macro_classes #micro_classes + quality_classes
for p in paths:
    path = os.path.join(root_path,p)
    for file in glob.glob(os.path.join(path,'*.xml')):
    #     print((file.split('/')[-1]).split('.')[0])
        tree = ET.parse(file)
        for elt in tree.iter():
            if((elt.tag == 'name')) :#& (elt.text == 'black_mark')):
            # if((elt.tag == 'name') & (elt.text not in ['double_ringmark','single_ringmark','arrow','model_no','lotmark'])):
                if elt.text not in remove_classes:
                    # print(file)
                    # print(elt.text ) 
                    # if elt.text in rename_classes:
                    elt.text = 'label'
                    count += 1
                else:
                    print(f"Not changed :: {elt.text} ")
                    not_change_count += 1
    # #     tree.find('//filename').text = (file.split('/')[-1]).split('.')[0] + '.jpg' 
        tree.write(file)

print(f"Changed : {count} labels")
print(f"Not Changed :{not_change_count} labels")   