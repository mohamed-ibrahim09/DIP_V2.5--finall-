import cv2
import numpy as np

clean_img = cv2.imread("images/afghan_girl.jpg")
noisy_images = []
for _ in range(10):  # Generate 10 noisy versions
    noise = np.random.normal(0, 25, clean_img.shape).astype(np.uint8)
    noisy_img = cv2.add(clean_img, noise)
    noisy_images.append(noisy_img)

for i, img in enumerate(noisy_images):
    cv2.imwrite(f"noise_images/noisy_afghan_girl_{i}.jpg", img)