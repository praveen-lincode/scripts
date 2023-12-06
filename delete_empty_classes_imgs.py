import os
import xml.etree.ElementTree as ET
import glob
# path = r'C:\Users\Admin\Downloads\CAM1_11_10_ANN\CAM1_11_10_ANN\CAM1_11_10\\'
path = glob.glob(r"D:\\lincode\\sansera\\Sansera_OCR_Jig_l_1\\ocr_b\\NO_OCR\\*.xml")

# print(path)

#path = r"C:\\\Users\\Admin\Downloads\Aug\without_Print\\"

def empty_names(path):
	# files = os.listdir(path)D:\te_1
	# for file in files:
	# 	if file.endswith('.xml'):
	# 		print(path + file)
	# 		tree = ET.parse(path+file)
	# 		root = tree.getroot()
	# 		l = [elt.tag for elt in root.iter()]
	# 		if 'name' not in l:
	# 			print(path+file)
	# 			# os.remove(path+file)
	# 			# os.remove(path+file.replace('.xml', '.jpg'))

	# 			# sp = file.split('.')
	# 			# print(path+sp[0]+'.'+sp[1]+'.jpg')
	# 			# os.remove(path+sp[0]+'.'+sp[1]+'.jpg')
	# 			# print(path+file.split('.')[0]+'.jpg')

	for file in path:
		tree = ET.parse(file)
		root = tree.getroot()
		l = [elt.tag for elt in root.iter()]
		if 'name' not in l:
			print(file)
			os.remove(file)
			os.remove(file.replace('.xml', '.jpg'))



empty_names(path)