import glob
import os 
import xml.etree.ElementTree as ET

classes = []
count_dic = {}
root = "C:\\Users\\Prave\\Downloads\\aug\\org_aug\\"


for f in range(1):
    count = 0
    path = f'{root}/batch_{f}'
    path = root #comment
    for file in glob.glob(os.path.join(path,'*.xml')):
        tree = ET.parse(file)
        for elt in tree.iter():
            if (elt.tag == 'name'):
                cls = elt.text
                if cls not in count_dic:
                    count_dic[cls] = 0
                count_dic[cls] += 1
    print(path)
    # print(count_dic)
print(count_dic)