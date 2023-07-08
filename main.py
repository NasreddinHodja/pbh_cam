#!/usr/bin/python3

import shutil
import os
import subprocess
import cv2 as cv
import pyexiv2
  
PICS_DIR = "./pics/"
PICSENDER_DIR = "/home/nasreddin/prog/pbh_picsender/"

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
  if not webcam.isOpened(): return

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
  shutil.copy(PICS_DIR + picture_name, PICSENDER_DIR + picture_name)
  cv.destroyAllWindows()
  return True

def get_email():
  print('\n\\ \\ [[ E-MAIL ]] ~ ', end='')
  email = input()
  os.system('clear')
  return email

def add_email_exif(path, email):
  metadata = pyexiv2.ImageMetadata(path)
  metadata.read()
  metadata['Exif.Image.Artist'] = pyexiv2.ExifTag('Exif.Image.Artist', email)
  metadata.write()

def main():
  webcam = cv.VideoCapture(0)
  email = get_email()

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
        add_email_exif(PICS_DIR + picture_name, email)
        subprocess.run([PICSENDER_DIR + "main.py"])
        break

  webcam.release()
  cv.destroyAllWindows()
  
if __name__ == "__main__":
  main()
