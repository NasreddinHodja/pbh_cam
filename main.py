#!/usr/bin/python3

import shutil
import os
import subprocess
import pygame.camera
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
    
def take_picture(webcam, window, clock, picture_name):
  run = True
  image = 0
  while run:
    clock.tick(100)
    for event in pygame.event.get():
      if event.type == pygame.QUIT: return False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: return False
        if event.key == pygame.K_RETURN:
          run = False

    camera_frame = webcam.get_image()
    image = camera_frame

    window.fill(0)
    window.blit(camera_frame, (0, 0))
    pygame.display.flip()
  
  pygame.image.save(image, PICS_DIR + picture_name)
  
  return True

def get_email():
  print('\n\\ \\ [[ E-MAIL ]] ~ ', end='')
  email = input()
  os.system('clear')
  return email

def add_email_exif(path, email):
  img = pyexiv2.Image(path)
  img.modify_exif({'Exif.Image.Artist': email})
  img.close()

def main():
  email = get_email()

  pygame.camera.init()
  camlist = pygame.camera.list_cameras()

  webcam = pygame.camera.Camera(camlist[2], (640, 480))

  window = pygame.display.set_mode(webcam.get_size())
  clock = pygame.time.Clock()
  webcam.start()

  picture_name = get_picture_name()
  
  if not take_picture(webcam, window, clock, picture_name): return

  increm_counter()
  add_email_exif(PICS_DIR + picture_name, email)

    # img = cv.imread(PICS_DIR + picture_name)
    # cv.imshow(picture_name, img)

    # key = cv.waitKey(0)
    # match key:
    #   # esc
    #   case 27: 
    #     cv.destroyAllWindows()
    #     continue 
    #   # enter
    #   case 13: 
    #     increm_counter()
    #     add_email_exif(PICS_DIR + picture_name, email)
    #     # subprocess.run([PICSENDER_DIR + "main.py"])
    #     break

if __name__ == "__main__":
  main()
