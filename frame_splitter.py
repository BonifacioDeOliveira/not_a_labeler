import argparse
import cv2
from tqdm import tqdm
import os

#Now load the video and split
def splitter(path, size):

    source_path = "source_videos/"+path
    video_name = path.split(".")
    destination_path = "splitted_frames/"+video_name[0]+"_frames"
    
    isdir = os.path.isdir(destination_path)
    if isdir == False:
        os.mkdir(destination_path)

    video = cv2.VideoCapture(source_path)
    if (video.isOpened() == False):
        return False
    
    for i in tqdm(range(size), desc="Splitting progress"):
        ret, frame = video.read()
        if ret == True:
            cv2.imwrite(destination_path+"/"+str(i)+".png", frame)

    video.release()
    return True

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("video_source_directory", type=str, help="source video directory")
    args = parser.parse_args()
    path = args.video_source_directory

    video = cv2.VideoCapture("source_videos/"+path)
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if splitter(path, length):
        print("Splitting successful")

    else:
        print("Error at video splitting")

