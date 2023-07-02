#!/usr/bin/python3

import shutil
import subprocess
import cv2 as cv
  
PICS_DIR = "./pics/"

def get_picture_name():
  with open("counter.txt", "r") as f:
    counter = int(f.readline())
    return str(counter).zfill(15) + ".png"

def increm_counter():
  with open("counter.txt", "r+") as f:
    counter = int(f.readline()) + 1
    f.seek(0)
    f.write(str(counter))
    
def take_picture(webcam, picture_name):
  if webcam.isOpened():
    validation, frame = webcam.read()
    while validation:
      validation, frame = webcam.read()
      cv.imshow("Webcam", frame)
      key = cv.waitKey(5)
      if key == -1: continue
      match key:
        # esc
        case 27: return False
        # return
        case 13: break

    cv.imwrite(PICS_DIR + picture_name, frame)
    cv.destroyAllWindows()
    return True

def main():
  webcam = cv.VideoCapture(0)

  while True:
    picture_name = get_picture_name()
    if not take_picture(webcam, picture_name): break

    img = cv.imread(PICS_DIR + picture_name)
    cv.imshow(picture_name, img)

    key = cv.waitKey(0)
    match key:
      # esc
      case 27: 
        cv.destroyAllWindows()
        continue 
      # enter
      case 13: 
        increm_counter()
        break

  webcam.release()
  cv.destroyAllWindows()
  
if __name__ == "__main__":
  main()