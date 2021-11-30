import cv2
import pygame

pygame.init()

def get_same_color(color_1,color_2):
    if abs(color_1[0]-color_2[0]) < 10 and abs(color_1[1]-color_2[1]) < 10 and abs(color_1[2]-color_2[2]) < 10 :
        return "0"
    return "1"

FILE = "video.mp4"
vidcap = cv2.VideoCapture(FILE)
success, image = vidcap.read()
cv2.imwrite("exemple.png", image)
count = 0
image_loading = pygame.image.load("exemple.png")
w, h = image_loading.get_width(),image_loading.get_height()
window = pygame.display.set_mode((w/2,h/2))
notes = {}
positions = []
image_loading = pygame.transform.scale(image_loading,(w/2,h/2))
while len(notes.keys()) < 67:
    window.blit(image_loading, (0, 0))
    for pos in positions:
        pygame.draw.rect(window,(255,0,0),pygame.rect.Rect(pos[1]/2-10,pos[0]/2-10,20,20))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            color = image_loading.get_at(e.pos)
            real_color = (color[2], color[1], color[0])
            pos = (e.pos[1]*2, e.pos[0]*2)
            notes[pos] = real_color
            positions.append(pos)
            print(pos, real_color)

pygame.quit()
files = []
for i in range(67):
    files.append(open(str(i)+".txt","w"))


while success:
    success, image = vidcap.read()
    for i in range(len(positions)):
        pos = positions[i]
        playing = get_same_color(image[pos[0]][pos[1]], notes[pos])
        files[i].write(playing)
    print(f'Read a new frame: ({count}) ', success)
    count += 1



