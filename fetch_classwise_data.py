import glob
import os 
import xml.etree.ElementTree as ET
import cv2


def create_folder(dir):
    if os.path.exists(dir):
        print(f"{dir} exists!!!")
        pass
    else:
        os.makedirs(dir)
        print(f"{dir} created!!")
    
    

def get_classwise_data(r , class_name , path):
    classes = []
    create_folder(class_name)
    for f in range(r):
        count = 0
        # path = f'./batch_{f}'
        # path = f'./all'
        # path = f'/home/lincode/Documents/Gokul/INDO_MIM/notebooks/yolov3/yolov3/annotations/val'
        # path = f'/home/lincode/Documents/Gokul/INDO_MIM/notebooks/yolov3/yolov3/annotations/XmlToTxt/train_xml_edited'
        for file in glob.glob(os.path.join(path,'*.xml')):
            # print((file.split('/')[-1]).split('.')[0])
            tree = ET.parse(file)

            for elt in tree.iter():
                if (elt.tag == 'name'):
                    classes.append(elt.text )
                if ((elt.tag == 'name') & ((elt.text == class_name) )):
                    img_name =  file.replace(".xml",".jpg")#(file.spilt("/")[-1])
                    img = cv2.imread(img_name)
                    # print(elt.text )
                    # elt.text = 'mdv001'

                    count += 1
        # # #     tree.find('//filename').text = (file.split('/')[-1]).split('.')[0] + '.jpg' 
                if count >0 :
                    print((file.split('/')[-1]).split('.')[0])
                    img_name = img_name.replace(f"\\hole_data\\",f"\\{class_name}\\")
                    file = file.replace(f"\\hole_data\\",f"\\{class_name}\\")
                    # print("----------------------------",file)
                    # img_name = img_name.replace(f"/batch_{f}/","/all/")
                    # file = file.replace(f"/batch_{f}/","/all/")
                    tree.write(file)
                    # print("--------------------",img_name)
                    cv2.imwrite(img_name ,img)
                    count = 0
        if count > 0:
            print(f'batch_{f}')
            print(count)   


classes = ["hole"]

for c_n in classes:
    get_classwise_data(r = 1 , class_name = c_n , path = "D:\\lincode\\magna\\ATV\\training_data\\hole_data")
    #"D:\\lincode\\europe\\fiasa\\images\\images\\fiasa_all_mosaic_2")
    # D:\\lincode\\magna\\new_segg\\shaft