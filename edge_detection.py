import cv2
import numpy as np
import os

# Ensure the edge_images directory exists
if not os.path.exists("edge_images"):
    os.makedirs("edge_images")

def sobel_filter(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise FileNotFoundError("NO IMAGE DETECTED!!!")

    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        gray = image
    else:
        raise ValueError("Unsupported image format")

    # Sobel X
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x = np.uint8(np.clip(np.absolute(sobel_x), 0, 255))

    # Sobel Y
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y = np.uint8(np.clip(np.absolute(sobel_y), 0, 255))

    # Combine X and Y
    sobel_combined = cv2.magnitude(np.float32(sobel_x), np.float32(sobel_y))
    sobel_combined = np.uint8(np.clip(sobel_combined, 0, 255))

    save_path = 'edge_images/sobel_combined.jpg'
    cv2.imwrite(save_path, sobel_combined)

    return save_path