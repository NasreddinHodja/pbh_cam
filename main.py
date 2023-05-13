#!/usr/bin/python3

import cv2 as cv

def take_picture(webcam):
  if webcam.isOpened():
    validation, frame = webcam.read()
    while validation:
      validation, frame = webcam.read()
      cv.imshow("Webcam", frame)
      key = cv.waitKey(5)
      if key == -1: continue
      print(key)
      match key:
        # esc
        case 27: return False
        # return
        case 13: break

    cv.imwrite("foto.png", frame)
    cv.destroyAllWindows()
    return True

def main():
  webcam = cv.VideoCapture(0)

  while True:
    if(not take_picture(webcam)): break

    img = cv.imread("foto.png")
    cv.imshow("foto.png", img)

    key = cv.waitKey(0)
    match key:
      # esc
      case 27: 
        cv.destroyAllWindows()
        continue 
      # enter
      case 13: break

  webcam.release()
  cv.destroyAllWindows()
  
if __name__ == "__main__":
  main()