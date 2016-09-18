from flask import Flask, request, render_template
import requests
import os
import cv2
import numpy as np
import base64
import json
import math

print(os.getcwd())

app = Flask(__name__)

def add_img(req_list, encoded_img, type, maxRes):

	req_list.append({
		'image' : {
			'content' : encoded_img
		},

		'features' : [{
			'type' : type,
			'maxResults' : maxRes,
		}]
	})

def populate_img_list(no_partitions, height, width, img):

	list_of_img = []

	d_x = int(width/int(math.sqrt(no_partitions)))

	d_y = int(height/round(no_partitions/int(math.sqrt(no_partitions))))

	for i in range(int(math.sqrt(no_partitions))):
		for j in range(int(round(no_partitions/int(math.sqrt(no_partitions))))):
			temp_img = img[j*d_y:(j+1)*d_y, i*d_x:(i+1)*d_x]
			cv2.imwrite("temp_img.jpg", temp_img)

			with open("temp_img.jpg", "rb") as f:
				encoded_img = base64.b64encode(f.read())

				list_of_img.append({ 'img_code':encoded_img , 'xpos' : (i*d_x + (i+1)*d_x)/2, 'ypos' : (j*d_y + (j+1)*d_y)/2})

	return list_of_img


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/find_features')
def find_features():

	print("getting args")
	lat = str(request.args.get('lat'))
	lng = str(request.args.get('lng'))
	head = str(request.args.get('head'))
	pitch = str(request.args.get('pitch'))
	fov = str(request.args.get('fov'))
	zoom = str(request.args.get('zoom'))
	number_partitions = int(str(request.args.get('partitions')))
	lang = str(request.args.get('lang'))

	print("zoom" + zoom)

	print("https://maps.googleapis.com/maps/api/streetview?location="+lat+","+lng+"&size=800x550&key=AIzaSyAi5tI84OEg4rQ05u7GPC9Ja9AIQ4z0ni4&heading="+head+"&pitch="+pitch)
	r = requests.get("https://maps.googleapis.com/maps/api/streetview?location="+lat+","+lng+"&size=800x550&key=AIzaSyAi5tI84OEg4rQ05u7GPC9Ja9AIQ4z0ni4&heading="+head+"&pitch="+pitch+"&fov="+fov)

	with open('image.jpg', 'wb') as f:
		f.write(r.content)

	filename = 'image.jpg'

	height = 535
	width = 600

	img = cv2.imread(filename)
	img = img[0:535, 0:600]

	# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# gray = np.float32(gray)
	# dst = cv2.cornerHarris(gray,2,3,0.04)

	# #result is dilated for marking the corners, not important
	# dst = cv2.dilate(dst,None)

	# # Threshold for an optimal value, it may vary depending on the image.
	# img[dst>0.01*dst.max()]=[0,0,255]

	# cv2.imshow('dst',img)
	# if cv2.waitKey(0) & 0xff == 27:
	#     cv2.destroyAllWindows()

	#First Pass - Split Image Into 2
	img_list = []
	used_labels = []
	label_list_response = []

	# img1 = img[0:height/2, 0:width]
	# cv2.imwrite("img1.jpg", img1)

	# with open("img1.jpg", "rb") as f:
	# 	encoded_img = base64.b64encode(f.read())

	img_code_list = populate_img_list(number_partitions, height, width, img)

	request_list = []

	for img_obj in img_code_list:
		add_img(request_list, img_obj['img_code'], 'LABEL_DETECTION', 9)

	api_request = {'requests' : request_list}

	json_data = json.dumps(api_request)

	r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAi5tI84OEg4rQ05u7GPC9Ja9AIQ4z0ni4", data=json_data)

	response_data = r.json()

	label_list = []

	for resp_obj in response_data['responses']:
		label_list.append(resp_obj['labelAnnotations'])

	for j in range(len(label_list)):
		for i in range(len(label_list[j])):
			if label_list[j][i]['description'] not in used_labels and float(label_list[j][i]['score']) > 0.84:
				used_labels.append(label_list[j][i]['description'])
				label_list_response.append({ 'desc' : label_list[j][i]['description'], 'xpos' : str(img_code_list[j]['xpos']), 'ypos' : str(img_code_list[j]['ypos'])})
				break;


	print(label_list_response)

	label_list_response_json = { 'response' : label_list_response}

	json_response = json.dumps(label_list_response_json)

	# for draw_obj in label_list_response:
	# 	cv2.putText(img, draw_obj['desc'], (int(draw_obj['xpos']), int(draw_obj['ypos'])), cv2.FONT_HERSHEY_SIMPLEX, .5,(255,255,255),2,4)

	# cv2.imshow('dst',img)
	# if cv2.waitKey(0) & 0xff == 27:
	#     cv2.destroyAllWindows()

	return json_response




if __name__ == "__main__":
    app.run()
