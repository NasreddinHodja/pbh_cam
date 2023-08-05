import pyexiv2

PIC_PATH = "./pics/000000000000007.png"
NEW_EXIF = "torporrr__"

img = pyexiv2.Image(PIC_PATH)
img.modify_exif({'Exif.Image.Artist': NEW_EXIF})
img.close()