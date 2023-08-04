import pygame.camera

pygame.camera.init()
camlist = pygame.camera.list_cameras()
print(camlist)

camera = pygame.camera.Camera(camlist[2], (640, 480))

window = pygame.display.set_mode(camera.get_size())
clock = pygame.time.Clock()
camera.start()

run = True
image = 0
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.ESC:
            run = False

    camera_frame = camera.get_image()
    image = camera_frame

    window.fill(0)
    window.blit(camera_frame, (0, 0))
    pygame.display.flip()

pygame.image.save(image, "filename.jpg")
pygame.quit()
exit()


# saving the image