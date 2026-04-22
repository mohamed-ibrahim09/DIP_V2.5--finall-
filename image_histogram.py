# histogram_operations.py

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def histogram_stretching(img_cv):
    if len(img_cv.shape) == 2:  # Grayscale image
        min_val = np.min(img_cv)
        max_val = np.max(img_cv)
        return img_cv if max_val == min_val else ((img_cv - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    else:  # Color image
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        min_val = np.min(v)
        max_val = np.max(v)
        v = v if max_val == min_val else ((v - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        return cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)

def histogram_equalization(img_cv):
    if len(img_cv.shape) == 2:  # Grayscale image
        return cv2.equalizeHist(img_cv)
    else:  # Color image
        ycrcb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)
        y = cv2.equalizeHist(y)
        return cv2.cvtColor(cv2.merge([y, cr, cb]), cv2.COLOR_YCrCb2BGR)

def show_histogram(img_cv, save_path="histogram_results/histogram.png"):
    os.makedirs("histogram_results", exist_ok=True)
    plt.figure(figsize=(8, 6))
    if len(img_cv.shape) == 2:
        plt.hist(img_cv.ravel(), 256, [0, 256], color='gray')
        plt.title('Grayscale Histogram')
    else:
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            plt.hist(img_cv[..., i].ravel(), 256, [0, 256], color=color, alpha=0.5)
        plt.title('Color Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.savefig(save_path)
    plt.close()
    return Image.open(save_path)
