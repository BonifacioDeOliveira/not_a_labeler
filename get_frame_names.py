import argparse
import cv2
import csv
import os

#Now load the video and split
def get_infos(path, size=None, mode="video"):
    video_name = path.split(".")
    destination_path = "video_faces_csv/"+video_name[0]+".csv"
    
    if mode == "frames":
        print("Frames mode is being used!! ")
        source_path = "splitted_frames/"+video_name[0]+"_frames"
        print(source_path)
    else:
        print("Video mode is being used!! ")
        source_path = "source_videos/"+path
        video = cv2.VideoCapture(source_path)
    
        if (video.isOpened() == False):
            return False

    with open(destination_path, mode='w') as names_file:
        names_writer = csv.writer(names_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        counter = 0
        if mode == "frames":
            for r, d, f in os.walk(source_path):
                files = sorted(f)
                for image in files:
                    counter+=1
                    image = cv2.imread(source_path+"/"+image)
                    cv2.imshow("image",image)
                    cv2.waitKey(1)
                    print("frame {} from {}".format(counter, len(files)))
                    names = input("Present persons: ")
                    if names == "close":
                        break
                    persons_names = names.split(",")
                    to_write = []
                    to_write.append(len(persons_names))
                    to_write.extend(persons_names)
                    names_writer.writerow(to_write)
            return True

        else:
            while(True):
                counter+=1
                ret, frame = video.read()
                if ret == True:
                    cv2.imshow('frame',frame)
                    cv2.waitKey(1)
                    print("frame {} from {} \n".format(counter, size))
                    names = input("Present persons: ")
                    if names == "close":
                        break
                    persons_names = names.split(",")
                    to_write = []
                    to_write.append(len(persons_names))
                    to_write.extend(persons_names)
                    names_writer.writerow(to_write)
            return True

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="video or frames")
    parser.add_argument("video_source_directory", type=str, help="source video directory")
    args = parser.parse_args()

    mode = args.source
    path = args.video_source_directory

    if mode == "video":
        video = cv2.VideoCapture("source_videos/"+path)
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    else:
        length = None

    if get_infos(path, length, mode):
        print("Splitting successful")

    else:
        print("Error at video splitting")
