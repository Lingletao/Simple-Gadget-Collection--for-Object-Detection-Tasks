import json
import os, sys

json_path = './train.json'	    	#json file path before modification
json_save_path = './train2.json'	#Modified json file save path 

file_in = open(json_path, "r")
file_out = open(json_save_path, "w")

jsondata = json.load(file_in)

specified_cls_name = "A" 		#Class name to be modified 
new_name = "AA"	    	 	    #New class name 

for item in jsondata['categories']:
    if specified_cls_name == item['supercategory']:
        item['supercategory'] = new_name
        item['name'] = new_name

file_out.write(json.dumps(jsondata))
file_in.close()
file_out.close()
