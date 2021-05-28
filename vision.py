import cv2
import numpy as np
import os

class Vision:
    @staticmethod
    def locateOnScreen(needle,haystack):
        needle_img = cv2.imread(needle)
        result = cv2.matchTemplate(haystack,needle_img,cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.75:
            return max_loc
        else: return (None,None)
    
    @staticmethod
    def locateAllOnScreen(needle,haystack):
        needle_img = cv2.imread(needle)
        result = cv2.matchTemplate(haystack,needle_img,cv2.TM_CCOEFF_NORMED)

        threshold = 0.9
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        locations = [(x+475,y+925) for x,y in locations]

        #getting rid of similar points
        d=55
        locations = {((x - (x % d)), (y - (y % d))) : (x,y) for x, y in locations}
        locations = list(locations)
        return locations
