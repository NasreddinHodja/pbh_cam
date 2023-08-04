#!/usr/bin/python3

import shutil
import os
import subprocess
import pygame.camera
import pyexiv2
  
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
  
  return image

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
  image = take_picture(webcam, window, clock, picture_name)
  running = True 
  while running:
    if not image: return

    for event in pygame.event.get():
      if event.type == pygame.QUIT: return
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          image = take_picture(webcam, window, clock, picture_name)
          continue
        if event.key == pygame.K_RETURN: 
          print('saved')
          pygame.image.save(image, PICS_DIR + picture_name)
          add_email_exif(PICS_DIR + picture_name, email)
          increm_counter()
          running = False

if __name__ == "__main__":
  main()
