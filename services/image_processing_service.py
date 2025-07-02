import cv2 
import numpy as np

def crop_ad_banner(image_path):
    print("image path is ",image_path)
    img = cv2.imread(image_path)
    original = img.copy()
    if img is None:
        print('Error loading the image')

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 200, 200])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cropped_images = []

    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(original, (x, y), (x+w, y+h), (0, 255, 0), 2)
        margin = 5
        crop = img[y+margin:y+h-margin, x+margin:x+w-margin]  
        if crop.size > 0:  # Check if crop is valid
            cropped_images.append(crop)  
    return cropped_images

