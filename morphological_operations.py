# import cv2
# import numpy as np

# def morphological_operations(img_path):

#     image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
#     if image is None:
#         print("Image not found.")
#         return

#     # Convert to grayscale if the image is colored
#     if len(image.shape) == 3 and image.shape[2] == 3:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     elif len(image.shape) == 2:
#         gray = image
#     else:
#         print("Unsupported image format.")
#         return

#     # Convert to binary
#     _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

#     kernel = np.ones((5, 5), np.uint8)

#     dilation = cv2.dilate(binary.copy(), kernel, iterations=1)
#     cv2.imwrite('morphology_images/dilation.jpg', dilation)

#     erosion = cv2.erode(binary.copy(), kernel, iterations=1)
#     cv2.imwrite('morphology_images/erosion.jpg', erosion)

#     opening = cv2.morphologyEx(binary.copy(), cv2.MORPH_OPEN, kernel)
#     cv2.imwrite('morphology_images/opening.jpg', opening)

#     internal_boundary = cv2.subtract(binary, erosion)
#     cv2.imwrite('morphology_images/internal_boundary.jpg', internal_boundary)

#     external_boundary = cv2.subtract(dilation, binary)
#     cv2.imwrite('morphology_images/external_boundary.jpg', external_boundary)

#     morph_gradient = cv2.subtract(dilation, erosion)
#     cv2.imwrite('morphology_images/morph_gradient.jpg', morph_gradient)

#     print("Morphological operations completed.")


# ==========================================================================================================

import cv2
import numpy as np
import os

# Ensure the output folder exists
output_dir = "morphology_images"
os.makedirs(output_dir, exist_ok=True)

# Common function to load image as grayscale
def load_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found.")
    return img

# Dilation operation
def dilation(image_path):
    img = load_image(image_path)
    kernel = np.ones((5,5), np.uint8)
    result = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, "dilation.jpg"), result)

# Erosion operation
def erosion(image_path):
    img = load_image(image_path)
    kernel = np.ones((5,5), np.uint8)
    result = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, "erosion.jpg"), result)

# Opening (Erosion followed by Dilation)
def opening(image_path):
    img = load_image(image_path)
    kernel = np.ones((5,5), np.uint8)
    result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(os.path.join(output_dir, "opening.jpg"), result)

# Internal Boundary = Original Image - Erosion
def internal_boundary(image_path):
    img = load_image(image_path)
    kernel = np.ones((5,5), np.uint8)
    erosion_img = cv2.erode(img, kernel, iterations=1)
    result = cv2.subtract(img, erosion_img)
    cv2.imwrite(os.path.join(output_dir, "internal_boundary.jpg"), result)

# External Boundary = Dilation - Original Image
def external_boundary(image_path):
    img = load_image(image_path)
    kernel = np.ones((5,5), np.uint8)
    dilation_img = cv2.dilate(img, kernel, iterations=1)
    result = cv2.subtract(dilation_img, img)
    cv2.imwrite(os.path.join(output_dir, "external_boundary.jpg"), result)

# Morphological Gradient = Dilation - Erosion
def morph_gradient(image_path):
    img = load_image(image_path)
    kernel = np.ones((5,5), np.uint8)
    dilation_img = cv2.dilate(img, kernel, iterations=1)
    erosion_img = cv2.erode(img, kernel, iterations=1)
    result = cv2.subtract(dilation_img, erosion_img)
    cv2.imwrite(os.path.join(output_dir, "morph_gradient.jpg"), result)