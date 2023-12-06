import glob
import os 
import xml.etree.ElementTree as ET
import cv2

path = '/home/lincode/Indo_medical/training/yolov3/yolov3/annotations/batch_9'

count = 0

for file in glob.glob(os.path.join(path,'*.xml')):
#     print((file.split('/')[-1]).split('.')[0])
    tree = ET.parse(file)
#     print(tree)
#     print((tree.find('//filename').text)) 
#     print((tree.find('//path').text))#.replace('_2_','_3_')) 
#     print((tree.find('//object//name').text))
#     try:
#         if tree.find('//object//name').text == 'overlapping' :
#             print((tree.find('//object//name').text))
#             tree.find('//object//name').text = 'overlap'
            
#     except :
#         print(file)
#         pass
#         print(file)
        

#     tree.find('//path').text = tree.find('//path').text.replace('_2_','_3_')
    for elt in tree.iter():
        if((elt.tag == 'name') &
           ((elt.text == 'blister') or (elt.text == 'crack') or 
            (elt.text == 'pip_break') or (elt.text == 'pin_hole'))):
        # if((elt.tag == 'name') & (elt.text not in ['double_ringmark','single_ringmark','arrow','model_no','lotmark'])):
            print(file)
            print(elt.text )
            elt.text = 'damage'
            count += 1
# #     tree.find('//filename').text = (file.split('/')[-1]).split('.')[0] + '.jpg' 
    tree.write(file)
print(count)   