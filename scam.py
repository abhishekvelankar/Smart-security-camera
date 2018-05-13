import cv2
import numpy as np
from twilio.rest import Client
from skimage.measure import compare_ssim
#create twilio account and add your details here
ACCOUNT_SID = ''
AUTH_TOKEN = ''
TWILIO_PHONE = ''
RECEIVER_PHONE = ''

def ssim(A,B):
	return compare_ssim(A,B,data_range=A.max()-A.min())

def mse(A,B):
	return ((A-B)**2).mean()
#creating twilio rest client

client = Client(ACCOUNT_SID,AUTH_TOKEN)

cap = cv2.VideoCapture('video.mp4')
#for using webcam
#cap = cv2.VideoCapture(0)
curr_frame=None
prev_frame=None
first_frame=True
frame_counter = 0
first_msg = True
while True:
	if frame_counter == 0:
		prev_frame = curr_frame
#taking frame from video
	_, curr_frame = cap.read()
	if curr_frame is None:
		break
	curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
	if first_frame:
		prev_frame = curr_frame
		first_frame = False
#counting ssim at interval of 10 frames
	if frame_counter == 9:
		ssim_index = ssim(curr_frame,prev_frame)
		frame_counter = 0


		if ssim_index < 0.8 and first_msg:
			client.messages.create(to=RECEIVER_PHONE, from_=TWILIO_PHONE,body="RUN RUN INTRUDER ALERT!!!!!!!!!!!!!!!!!!!")
			first_msg = False



	cv2.imshow('app',curr_frame)
	frame_counter = frame_counter + 1
#waiting for camera to take frame from video.
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

"""
ACCOUNT SID
ACabd42fb89995a766c6d8f1b997383c0c

AUTH TOKEN
eb1d3221924a4dd5995bd0777efa0811
"""
