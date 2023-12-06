import os
import xml.etree.ElementTree as ET
import shutil

path = r"D:\lincode\conrod\demo_sep_23\data\\"
# out = r"C:\Users\Public\bharati\car_da.v1i.voc\out\\"

def empty_names(path):
	files = os.listdir(path)
	for file in files:
		if file.endswith('.xml'):
			tree = ET.parse(path+file)
			root = tree.getroot()
			l = [elt.tag for elt in root.iter()]
			if 'name' not in l:
				print(path+file)
				# print(path+file.replace('.xml', '.jpg'))
				os.remove(path+file)
				os.remove(path+file.replace('.xml', '.jpg'))

				### moving images and xml
				 # shutil.move(path+file,out+file)
				 # shutil.move(path+file.replace('.xml', '.jpg'),out+file.replace('.xml', '.jpg'))



				# sp = file.split('.')
				# print(path+sp[0]+'.'+sp[1]+'.jpg')
				# os.remove(path+sp[0]+'.'+sp[1]+'.jpg')
				# print(path+file.split('.')[0]+'.jpg')
				# shutil.move(path+file,out+file)s
					

empty_names(path)