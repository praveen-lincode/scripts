
import xml.etree.ElementTree as ET
from pascal_voc_writer import Writer
import os






main_path = r"C:\\Users\\Prave\\Downloads\\aug\\org_aug\\"


def delete_classname(xml_file, class_name):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for object in root.findall('object'):
        name = object.find('name').text
        
        if name == class_name:
            print(xml_file, class_name)
            root.remove(object)	

    tree.write(xml_file)


def get_all_classes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    classes = []
    for object in root.findall('object'):
        name = object.find('name').text
        classes.append(name)
    return classes



res = os.walk(main_path)

for i in res:
    root = i[0]
    folders = i[1]
    files = i[2]

    for file in files:
        if file.endswith('.xml'):

            # print(file)
            xml_file = root + '\\' + file
            print(xml_file)
            all_classes = get_all_classes(xml_file)
            print(all_classes)

            for class_name in all_classes:
                if class_name == 'stud_ab' or class_name == 'bg' or class_name == 'burr':
                    delete_classname(xml_file, class_name)
                # else:
                #     delete_classname(xml_file, class_name)

