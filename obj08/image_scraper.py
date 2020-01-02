#!/usr/bin/python
import json
import requests
import base64
import os

print "Making CAPTEHA request... "
response = requests.get("https://fridosleigh.com/api/capteha/request")

print "Processing response... "
response_json = json.loads(response.text);
images = response_json['images']
print str(len(images)) + " images found in response"

print "Searching for image types... "
types = response_json['select_type'].replace(", and ", ", ").split(', ')
for type in types:
	if not os.path.exists("training_data/"+type):
		os.mkdir("training_data/"+type)
		print "  > Found new type '" + type + "'"

print "Saving images... "
new_images = 0
dup_images = 0
for image in images:
	if os.path.exists("unlabelled_data/"+image['uuid']+".png"):
		dup_images = dup_images + 1
	else:
		fo = open("unlabelled_data/"+image['uuid']+".png",'w')
		fo.write(base64.decodestring(image['base64']))
		fo.close()
		new_images = new_images + 1

print "Finished! " + str(new_images) + " images saved, " + str(dup_images) + " ignored as duplicates."





