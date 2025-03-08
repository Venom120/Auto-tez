import cv2 as cv
import numpy as np
from PIL import Image

class Vision:
    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_GRAYSCALE)

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.7, debug_mode=False, is_grayscale=False):
        if not is_grayscale:
            haystack_img = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
            
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        if len(locations) == 0:
            return None 
        
        loc=locations[0]
        rect = [int(loc[0]), int(loc[1]), int(loc[0] + self.needle_w), int(loc[1] + self.needle_h)]

        if debug_mode:
            print(f"Needle found at ({rect[0]} {rect[1]}) till ({rect[2]} {rect[3]})")
            # cv.imshow('Matches', haystack_img)
            # cv.waitKey()
            # cv.imwrite('result_click_point.jpg', haystack_img)

        return rect
    
    

    def ball_crossed(self, img, threshold=40):
        # Convert to grayscale for faster processing
        gray_pixels = np.linalg.norm(img, axis=1)  # Compute intensity
        # Compute absolute differences
        diff = np.abs(np.diff(gray_pixels))

        # Find the first occurrence where the change exceeds the threshold
        crossing_index = np.argmax(diff >= threshold)

        return crossing_index if diff[crossing_index] > threshold else None