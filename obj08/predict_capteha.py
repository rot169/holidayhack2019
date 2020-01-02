#!/usr/bin/python3
import json
import requests
import base64
import os
import tensorflow as tf
import numpy as np
import threading
import queue
import time
import sys

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def predict_image(q, sess, graph, image_bytes, img_full_path, labels, input_operation, output_operation):
    image = read_tensor_from_image_bytes(image_bytes)
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: image
    })
    results = np.squeeze(results)
    prediction = results.argsort()[-5:][::-1][0]
    q.put( {'img_full_path':img_full_path, 'prediction':labels[prediction].title(), 'percent':results[prediction]} )

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph

def read_tensor_from_image_bytes(imagebytes, input_height=299, input_width=299, input_mean=0, input_std=255):
    image_reader = tf.image.decode_png( imagebytes, channels=3, name="png_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.compat.v1.Session()
    result = sess.run(normalized)
    return result


# Loading the Trained Machine Learning Model created from running retrain.py on the training_images directory
graph = load_graph('/tmp/retrain_tmp/output_graph.pb')
labels = load_labels("/tmp/retrain_tmp/output_labels.txt")

# Load up our session
input_operation = graph.get_operation_by_name("import/Placeholder")
output_operation = graph.get_operation_by_name("import/final_result")
sess = tf.compat.v1.Session(graph=graph)
q = queue.Queue()

# Get a CAPTEHA challenge and extract the relevant data
print("Getting CAPTEHA challenge... ")
challenge = requests.get("https://fridosleigh.com/api/capteha/request")
challenge_json = json.loads(challenge.text);
images = challenge_json['images']
types = challenge_json['select_type'].replace(", and ", ", ").split(', ')
challenge_cookie = challenge.headers['Set-Cookie'].split(';')[0]

# Send each image to our ML model
print("Analysing  images... ")
for image in images:
	# We don't want to process too many images at once. 10 threads max
	while len(threading.enumerate()) > 10:
		time.sleep(0.0001)
	image_data = base64.decodebytes(bytes(image['base64'],'utf8'))
	image_name = image['uuid']
	threading.Thread(target=predict_image, args=(q, sess, graph, image_data, image_name, labels, input_operation, output_operation)).start()

# Wait for completion
print('Waiting For Threads to Finish...')
while q.qsize() < len(images):
	time.sleep(0.001)

# Loop through results, identifying images which are in the CAPTEHA challenge categories
prediction_results = [q.get() for x in range(q.qsize())]
matching_uuids = []
for prediction in prediction_results:
	if prediction['prediction'] in types:
		print(">>>> UUID {img_full_path} is a {prediction} ({percent:.2%} accuracy)".format(**prediction))
		matching_uuids.append(prediction['img_full_path'])
	else:
		print("     UUID {img_full_path} is a {prediction} ({percent:.2%} accuracy)".format(**prediction))

# Formulate and submit the CAPTEHA response
print("Sending CAPTEHA response...")
response = requests.post(
    'https://fridosleigh.com/api/capteha/submit',
    data={'answer': ','.join(matching_uuids)},
    headers={'Cookie': challenge_cookie},
)

print(response.content)







