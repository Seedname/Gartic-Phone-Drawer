import pyautogui
from PIL import Image, ImageOps
import ctypes

user32 = ctypes.windll.user32
w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

sx, sy = w/2565, h/1440

im = Image.open('images/IMAGE_NAME.png', 'r')
betterColors = False
pen = 2

sizes = [2, 8, 15, 25, 40]
size_poses = []

for i in range(0, len(sizes)):
    size_poses.append(((669+i*90)*sx, 1343*sy))

bucket_pos = (2141, 913)
pen_pos = (2045, 607)
middle_pos = (1281, 854)

scale = sizes[pen-1]
size_pos = size_poses[pen-1]

colors = [(0, 0, 0), (102, 102, 102), (32, 79, 198), (255, 255, 255), (170, 170, 170), (97, 198, 250), (49, 114, 45), (140, 26, 16), (140, 70, 32), (81, 173, 76), (234, 51, 41), (238, 128, 63), (167, 115, 48), (140, 26, 77), (189, 97, 91), (246, 195, 76), (234, 51, 141), (242, 178, 170)]
colors_pos = [] 
for i in range(0, 6):
    colors_pos.append((390*sx, (i*70+584)*sy))
    colors_pos.append((460*sx, (i*70+584)*sy))
    colors_pos.append((525*sx, (i*70+584)*sy))

# newC = []

# def convert(num):
#     blue = num & 255
#     green = (num >> 8) & 255
#     red = (num >> 16) & 255
#     return (blue, green, red)

# for i in range(0, len(colors_pos)):
#     c = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), colors_pos[i][0], colors_pos[i][1])

#     newC.append(convert(c))

# print(newC)
# a


bounds = [(606*sx, 458*sy),  (1950*sx, 1211*sy)]

width = bounds[1][0] - bounds[0][0]
height = bounds[1][1] - bounds[0][1]

resized = im.resize((int(width/scale), int(height/scale)), Image.LANCZOS)
resized.convert('RGB')

pix_val = list(resized.getdata())

distance = []
mapped = []
count = [0] * len(colors)

contiguous_pixels = []
lastPixel = -1
for i in range(0, len(pix_val)):
    # useWeird = False
    # if isinstance(pix_val[i], int): 
    #     useWeird = True

    for j in range(0, len(colors)):
        # if not useWeird: 
        red_diff = (pix_val[i][0] - (colors[j][0]))**2
        green_diff = (pix_val[i][1] - (colors[j][1]))**2
        blue_diff = (pix_val[i][2] - (colors[j][2]))**2
        # else:
        # red_diff = (pix_val[i] - (colors[j][0]))**2
        # green_diff = (pix_val[i] - (colors[j][1]))**2
        # blue_diff = (pix_val[i] - (colors[j][2]))**2

        if betterColors:
            R = (pix_val[i][0] + int(colors[j][0]))/2
            # else: R = (pix_val[i] + int(colors[j][0]))/2

            if R < 128:
                distance.append( (2*red_diff + 4*green_diff + 3*blue_diff)**1/2 ) 
            else:
                distance.append( (3*red_diff + 4*green_diff + 2*blue_diff)**1/2 )
        else: 
            distance.append( (red_diff + green_diff + blue_diff)**1/2 )
    
    min = 3 * 255**2 + 1
    min_index = -1
    for j in range(0, len(distance)):
        if distance[j] < min: 
            min = distance[j]
            min_index = j

    if(lastPixel != min_index):
        contiguous_pixels.append(0)
        lastPixel = min_index

    contiguous_pixels[len(contiguous_pixels)-1] += 1
    mapped.append(min_index)
    count[min_index] += 1
    distance = []

maxValue = -1
maxIndex = -1
for i in range(0, len(count)):
    if count[i] > maxValue: 
        maxValue = count[i]
        maxIndex = i


pyautogui.PAUSE = 0.00001

pyautogui.click(bucket_pos)
pyautogui.click(colors_pos[maxIndex])
pyautogui.click(middle_pos)
pyautogui.click(pen_pos)

pyautogui.click(size_pos)
lastColor = -1
currentChange = -1

i = 0
while i < len(mapped):

    j = int(i/int(width/scale))
    im = i % int(width/scale)
    if mapped[i] != maxIndex: 
        if mapped[i] != lastColor:
            pyautogui.click(colors_pos[mapped[i]])
            lastColor = mapped[i]
            currentChange += 1
            i += 1
            pyautogui.click(im*scale + bounds[0][0], j*scale + bounds[0][1])
        else:
            pyautogui.moveTo(im*scale + bounds[0][0], j*scale + bounds[0][1])
            pyautogui.mouseDown()
            i += contiguous_pixels[currentChange]
            if j != int(i/int(width/scale)):
                i -= i % int(width/scale)
            
            pyautogui.moveTo(i*scale + bounds[0][0], j*scale + bounds[0][1])
            pyautogui.mouseUp()
            i += 1
    
    else:
        i += contiguous_pixels[currentChange]
        currentChange += 1
        

        