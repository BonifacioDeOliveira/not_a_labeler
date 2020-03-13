import time
import cv2 
import subprocess
import numpy as np

video_mode = int(input(" 1 - Record videos by frames number \n 2 - Record videos by time "))
grayscale = input(" Want grayscale frames [y/n]: ")
video_name = input(" Video name and format ( <name>.<format> ): ")

counter = 0

def check_if_picamera():
    try:
        shell_output = subprocess.check_output("vcgencmd get_camera", shell=True)
        shell_output = str(shell_output)
        avaliable = "detected=1" in shell_output
    except:
        avaliable = False
    return avaliable

has_picamera = check_if_picamera()

if has_picamera:
    from picamera.array import PiRGBArray
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.5)
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array

else:
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()

frame_width = 640
frame_height = 480
 
out = cv2.VideoWriter("recorded_videos/"+video_name,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

if video_mode == 1:
    number_of_frames = int(input(" Number of frames: "))
    
if video_mode == 2:
    recording_time = int(input("Recording time (Minutes): "))
    start_time = time.time()

while(True):

    if has_picamera == False:
        ret, frame = capture.read()
    
    else:
        rawCapture.truncate(0)
        camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array

    if grayscale in ["y", "Y"]:
        #frame = np.array(frame, dtype=np.uint8)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    

    if video_mode == 1:
        counter += 1
        if counter <= number_of_frames:
            out.write(frame)
        else:
            break
    
    if video_mode == 2:
        current_time = time.time() - start_time
        if (current_time/60) <= recording_time:
            out.write(frame)
        else:
            break

    cv2.imshow('frame',frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

if has_picamera == False:    
    capture.release()

out.release()
        


