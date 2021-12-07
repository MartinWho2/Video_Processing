import cv2
import pygame

pygame.init()
LIGHT_RIGHT_HAND = (90,225,160)
DARK_RIGHT_HAND = (25,160,90)
RIGHT_HAND = [LIGHT_RIGHT_HAND,DARK_RIGHT_HAND]
LIGHT_LEFT_HAND = (200,170,130)
DARK_LEFT_HAND = (170,115,65)
LEFT_HAND = [LIGHT_LEFT_HAND,DARK_LEFT_HAND]
def get_same_color(color_now,color_2,iterate=True):
    if abs(color_now[0]-color_2[0]) < 15 and abs(color_now[1]-color_2[1]) < 15 and abs(color_now[2]-color_2[2]) < 15 :
        return "0"
    if iterate:
        return get_hand_playings(LEFT_HAND,RIGHT_HAND,color_now)
    else:
        return "1"

def get_hand_playings(left_hand,right_hand,color):
    print(f"The color is {color}")
    if get_same_color(left_hand[0],color,iterate=False) == "0" or get_same_color(left_hand[1],color,iterate=False) == "0":
        return "1"
    elif get_same_color(right_hand[0],color,iterate=False) == "0" or get_same_color(right_hand[1],color,iterate=False) == "0":
        return "2"
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

begin = False
while success:
    success, image = vidcap.read()
    if not begin:
        for i in range(len(positions)):
            pos = positions[i]
            if get_same_color(image[pos[0]][pos[1]], notes[pos]) == "1":
                begin = True
    if begin:
        for i in range(len(positions)):
            pos = positions[i]
            playing = get_same_color(image[pos[0]][pos[1]], notes[pos])
            files[i].write(playing)
        print(f'Read a new frame: ({count}) ', success)
    count += 1



