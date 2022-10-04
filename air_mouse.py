# Made by Bhavneek, following tutorial by freecodecamp.org


# Import Statements
import math
from PyInstaller.utils.hooks import collect_submodules
import cv2 as cv
import numpy as np
import hand_module as hm
import time
import autopy as apy
import autopy.mouse


# Declaring global variables
x0, x1, x2, x3, x4, y0, y1, y2, y3, y4 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
length1, length2 = 0, 0
plocx, plocy = 0, 0
clocx, clocy = 0, 0
w, h = 640, 480
ptime = 0


# Instance Generator
cap = cv.VideoCapture(0)
button = apy.mouse.Button
det = hm.hand_detector(max_hands=1)



# Display size set/read
cap.set(3, w)
cap.set(4, h)
w_screen, h_screen = apy.screen.size()


while True:
    success, img = cap.read()    # success = whether we got a frame or not, if yes, it returns img

    # Find hands and return loci list
    img = det.find_hands(img)
    list = det.find_position(img)



    cv.rectangle(img, (100, 100), (w - 200, h - 200), (0, 255, 0), 2)  # draw rectangle around which it read hand position


    # check which fingers are up
    up_fingers = []
    if len(list) != 0:
        x4, y4 = list[20][0], list[20][1]   # location of little fingertip
        x3, y3 = list[16][0], list[16][1]   # location of ring fingertip
        x2, y2 = list[12][0], list[12][1]   # location of middle fingertip
        x1, y1 = list[8][0], list[8][1]     # location of index fingertip
        x0, y0 = list[4][0], list[4][1]     # location of thumb tip


        # Getting length between thumb and pinky, thumb and index
        length1 = math.hypot(x1 - x0, y1 - y0)
        length2 = math.hypot(x4 - x0, y4 - y0)


        # Getting how many fingers (except thumb) are up
        for i in range(8, 21, 4):
            if list[i][1] > list[i - 2][1]:
                up_fingers.append(0)
            else:
                up_fingers.append(1)


    if len(up_fingers) != 0:

        # Adding click functionality
        if up_fingers.count(1) == 4:
            if length1 < 40:
                apy.mouse.click()
            elif length2 < 40:
                apy.mouse.click(button.RIGHT)

        # Condition for moving
        if up_fingers.count(1) == 1 & up_fingers[0] == 1:

            # Converting from reading area to screen area
            x3 = np.interp(x1, (100, w - 200), (0, w_screen))
            y3 = np.interp(y1, (100, h - 200), (0, h_screen))

            # Smoothing
            clocx = plocx + (x3 - plocx) / 11
            clocy = plocy + (y3 - plocy) / 11

            # incase the hand goes out of detecting area
            try:
                apy.mouse.move(w_screen - clocx, clocy)
            except ValueError:
                continue

        # updating values of position for smoothing
        plocx, plocy = clocx, clocy


    # Putting FPS on corner
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv.putText(img, str(int(fps)), (10, 30), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)


    # Adding condition for closing the window
    if success:
        cv.imshow('AirMouse by Bhavneek Singh: Press "q" to exit', img)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
        if bool(cv.getWindowProperty('AirMouse by Bhavneek Singh: Press "q" to exit', cv.WND_PROP_VISIBLE)) == 0:
            break
    else:
        break
