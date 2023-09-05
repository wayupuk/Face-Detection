import cv2 
import datetime
import time as timer
from threading import Thread
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ultralytics import YOLO
# myfacedetector-001.xml
model = YOLO("wayaj.pt")
# model = YOLO("yolov5x.pt")
# face_detect = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")

class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
	
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
	def read(self):
		# return the frame most recently read
		return self.frame
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True







# if __name__ == "__main__":

#     model_path = 'C:\VScode\PYTHON\detect.tflite'
#     label_path = 'C:\VScode\PYTHON\labelmap.txt'

#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
#     cap.set(cv2.CAP_PROP_FPS, 15)

#     interpreter = load_model(model_path)

#     input_details = interpreter.get_input_details()

#     # Get Width and Height
#     input_shape = input_details[0]['shape']
#     height = input_shape[1]
#     width = input_shape[2]

#     # Get input index
#     input_index = input_details[0]['index']

#     # Process Stream

# model_path = "PYTHON/sex_classifer.tflite"
# interpreter = load_model(model_path)
# ap = argparse.ArgumentParser()
# ap.add_argument("-n", "--num-frames", type=int, default=100,
# help="# of frames to loop over for FPS test")
# ap.add_argument("-d", "--display", type=int, default=-1,
# help="Whether or not frames should be displayed")
# args = vars(ap.parse_args())

print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
co = []
width = 640
height = 480
count = 0
detect = []
delay = 0
CPbf = 0
CPaf = 0
boo = ""
m = 1
n = 0
arr = []
def center_point(x,y,w,h):
	cx = int((x+w)/2)
	cy = int((y+h)/2)
	return cx,cy	

	# loop over some frames...this time using the threaded stream
firsttime = timer.time()
while True:
	detect = []
	detect_count = []
	
	time = datetime.datetime.now()
	maintime = time.strftime("%d-%m-%y")
	day = time.strftime('%d')
	month = time.strftime('%m')
	frame = vs.read()
	
	frame = cv2.flip(frame,1)

	frame = cv2.resize(frame,(640,480))
	frame_crop = cv2.resize(frame,(640,480))
	cv2.line(frame_crop,(553,140),(49,140),(255,255,0),2)
	cv2.line(frame_crop,(553,320),(49,320),(255,255,0),2)
	cv2.line(frame_crop,(49,0),(49,480),(255,255,0),2)
	cv2.line(frame_crop,(553,0),(553,480),(255,255,0),2)
	# Detection and Count section

		# Processing outputs
	results = model(frame)
	# print("results:", results)
	box = results[0].boxes
	people = len(box)
	if len(box) > 0:
		
		for i in range(len(box.xyxy)):
			cor =box.xyxy[i]
			# print("corrrrrr: ",box.xyxy)
			# print(len(cor))
			if len(cor) == 0:
				continue
			else:
				# print(cor[0])
				co = cor[0]
				# print("co:",co)
				x = round(cor[0].item())
				y = round(cor[1].item())
				w = round(cor[2].item())
				h = round(cor[3].item())
				# cv2.rectangle(frame,(x,y),(w,h),(70,100,20),2)
				center = center_point(x,y,w,h)
				cv2.rectangle(frame_crop, (x,y), (w,h), (70,100,20), 2)
				cv2.circle(frame_crop,(center),4,(0,0,255),-2)
				# Putting the boxes and labels on the image
				if 553>((x+(w))/2)>49 and 140<((y+(h))/2)<320:
					
					# center = center_point(x,y,w,h)
					# cv2.circle(frame,(center),4,(0,0,255),-1)
					countp = center_point(x,y,w,h)
					detect.append(countp)
					detect_count.append([x,y,w,h])
					# print(countp)
					# print(type(detect))
					CPaf = len(detect_count)
					for (x,y) in detect :
						if 320>y>140 and 553>x>49:
							if len(detect_count) > 0 :
								print("detc: "+str(len(detect_count)))
								
							else:
								CPaf = 0
								print(len(detect_count))
								print("Cpaf:"+str(type(CPaf)))	
							if CPbf == CPaf :
								print("CPbf == CPaf")
								break
								
							else :
								if CPaf == 0 :
									CPbf = 0
									print("CPBF=0")
								else :
									if CPaf > CPbf:
										print("cpaf :",CPaf)
										print("cpaf :",CPbf)
										count = count + int(CPaf-CPbf)
										n+=1
										CPbf = CPaf
									
			
	print(detect_count)
	print("CPaf:"+str(CPaf))
	print("CPbf:"+str(CPbf))
	if n > 0:
		if len(detect) > 1 :
			detect = detect.reverse()
	if CPbf>CPaf:
		CPbf = CPaf
	print(people)
	if people == 0:
		CPbf = 0
		CPaf = 0
	cv2.putText(frame_crop,"Datetime: "+ maintime,(280,530),cv2.FONT_HERSHEY_TRIPLEX,0.5,(28,234,65),1,cv2.LINE_AA)
	cv2.putText(frame_crop,"Count : "+str(count),(360,70),cv2.FONT_HERSHEY_TRIPLEX,1,(28,234,65),1)
	cv2.imshow("corp",frame_crop)
	cv2.imshow("Frame", frame)
	ended = timer.time()
	print(ended-firsttime)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
	# update the FPS counter
	# stop the timer and display FPS information		# print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		# print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		# do a bit of cleanup
	
	# if endedtime == "20-40":
	# 	break

cv2.destroyAllWindows()
vs.stop()
endedtime = time.strftime("%H-%M")
dayl = [int(i) for i in day.split() if i.isdigit()]

# Database

actualday = dayl[0]
print(actualday)
actualday +=1
print(month)
scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
keys = "PYTHON\keys.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(keys, scopes) #access the json key you downloaded earlier 
file = gspread.authorize(credentials) # authenticate the JSON key with gspread
sheet = file.open("project") #open sheet
sheettt = sheet.sheet1 #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
# dayn = int(sheettt.acell('D1').value)
sheettt.update_acell('A'+ str(actualday),str(maintime))

sheettt.update_acell('C'+ str(actualday),str(endedtime))
print(sheettt.acell('B'+ str(actualday)).value)
if sheettt.acell('B'+ str(actualday)).value != None:
	sheettt.update_acell('B'+ str(actualday),str(count+int(sheettt.acell('B'+ str(actualday)).value)))
else:
	sheettt.update_acell('B'+ str(actualday),str(count))
ch = "=choose(WEEKDAY("
ab = "A"+str(actualday)+",2)"
daya = ',"mon","tue","wed","thu","fri","sat","sun")'
alll = ch + ab + daya
sheettt.update_acell('D'+str(actualday),alll)
# dayn +=1
sheettt.update_acell('D1',str(actualday))

print("success")