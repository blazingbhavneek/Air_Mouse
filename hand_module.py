# Made by Bhavneek, following tutorial by freecodecamp.org

################ Import Statements #################

import math
from PyInstaller.utils.hooks import collect_submodules
import cv2 as cv
import mediapipe as mp


#####################################################


################# Defining Class ####################

class hand_detector:
    def __init__(self,
                 mode=False,
                 max_hands=2,  # number of hands it's allowed to detect
                 model_complexity=1,  # parameter of method mediapipe.hand
                 detection_confidence=0.5,  # only detect if confidence is > this value
                 tracking_confidence=0.5):  # track only if confidence > this value

        ######### Parameters for mediapipe.hands #########
        self.mode = mode
        self.model_complexity = model_complexity
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        ##################################################

        ########## Part of mediapipe that detects hands ######
        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(self.mode, self.max_hands, self.model_complexity, self.detection_confidence,
                                        self.tracking_confidence)

        self.mp_draw = mp.solutions.drawing_utils  # Instance of object that draws hand mesh on img
        ######################################################

        ####### In-class variables ##########
        self.results = None
        #####################################


    ###### this function will update list of loci of points on fingers and return image with drawn hand points ######
    def find_hands(self, img):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # Conversion of BGR to RGB
        self.results = self.hands.process(
            img_rgb)  # method 'process' on an in-class instance of mediapipe.solutions.hands.Hands

        if self.results.multi_hand_landmarks:  # results have a list multi_hand_landmarks of format [ nth hand, [object landmark which contains coordinates of 21 representing points]]
            for index in range(len(self.results.multi_hand_landmarks)):

                hand_lms = self.results.multi_hand_landmarks[index]
                # hand_lms contains id of hand part and its corresponding location in ratio

                self.mp_draw.draw_landmarks(img, hand_lms,
                                            self.mp_hand.HAND_CONNECTIONS)  # drawing using instance of draw util
        return img
    ############################################


    ###### This func will return a list containing list of x,y coordinates of nth hand point ###########
    def find_position(self, img, hand_index=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand_lms = self.results.multi_hand_landmarks[hand_index]
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([cx, cy])
        return lm_list
    ####################################################################################################