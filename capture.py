  
from PIL import ImageGrab
import cv2
import numpy as np


class screenCapture:

    @staticmethod
    def screen_shot():
        img = ImageGrab.grab()
        img = np.array(img)
        img2 = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        return img2
