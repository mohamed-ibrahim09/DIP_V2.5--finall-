# import customtkinter as ctk
# from tkinter import filedialog, messagebox
# from PIL import Image
# import numpy as np
# import cv2
# import os

# # ========== Brightness Function ==========
# def add_brightness(img, value=50):
#     modified = img.copy()
#     if len(modified.shape) == 2:  # Grayscale
#         modified = cv2.add(modified, value)
#     elif len(modified.shape) == 3 and modified.shape[2] == 3:  # Color
#         modified = cv2.add(modified, np.array([value, value, value]))
#     else:
#         raise ValueError("Unsupported image format")
#     return modified

# # ========== Image Resize for display ==========
# def image_size(img, maxSize):
#     w, h = img.size
#     if w > h:
#         w, h = maxSize, int(h * (maxSize / img.width))
#     else:
#         h, w = maxSize, int(w * (maxSize / img.height))
#     return (w, h)

# # ========== Main App ==========
# app = ctk.CTk()
# app.geometry("900x600")
# app.title("Brightness with Popup")

# image_pil = None
# image_ctk = None
# image_processed = None

# # ========== Left Frame ==========
# left_frame = ctk.CTkFrame(app, width=200)
# left_frame.pack(side="left", fill="y", padx=10, pady=10)
# left_frame.pack_propagate(False)

# # ========== Right Frame ==========
# right_frame = ctk.CTkFrame(app)
# right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
# right_frame.pack_propagate(False)

# # ========== Upload Image ==========
# def upload_image():
#     global image_pil, image_ctk
#     path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
#     if path:
#         image_pil = Image.open(path)
#         resized = image_size(image_pil, 300)
#         image_ctk = ctk.CTkImage(light_image=image_pil, size=resized)
#         img_label.configure(image=image_ctk, text="")

# # ========== Popup Window ==========
# def open_popup():
#     if image_pil is None:
#         messagebox.showinfo("Error", "Please upload an image first.")
#         return

#     popup = ctk.CTkToplevel(app)
#     popup.title("Adjust Brightness")
#     popup.geometry("300x150")

#     label = ctk.CTkLabel(popup, text="Enter Brightness Value:")
#     label.pack(pady=5)

#     entry = ctk.CTkEntry(popup, placeholder_text="Default = 50")
#     entry.pack(pady=5)

#     def apply_brightness():
#         try:
#             val = entry.get()
#             brightness = int(val) if val else 50

#             img_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
#             result_cv = add_brightness(img_cv, brightness)
#             result_pil = Image.fromarray(cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB))
#             image_result = ctk.CTkImage(light_image=result_pil, size=image_size(result_pil, 400))
#             result_label.configure(image=image_result, text="")
#             result_label.image = image_result
#             popup.destroy()
#         except Exception as e:
#             messagebox.showerror("Error", str(e))

#     apply_btn = ctk.CTkButton(popup, text="Apply", command=apply_brightness)
#     apply_btn.pack(pady=10)

# # ========== Widgets in Left Frame ==========
# upload_btn = ctk.CTkButton(left_frame, text="Upload Image", command=upload_image)
# upload_btn.pack(pady=10)

# apply_btn = ctk.CTkButton(left_frame, text="Apply Brightness", command=open_popup)
# apply_btn.pack(pady=10)

# img_label = ctk.CTkLabel(left_frame, text="No Image")
# img_label.pack(pady=20)

# # ========== Right Frame Output ==========
# result_label = ctk.CTkLabel(right_frame, text="Result will appear here")
# result_label.pack(pady=20)

# app.mainloop()

# import customtkinter as ctk
# from tkinter import filedialog, messagebox
# from PIL import Image
# import numpy as np
# import cv2

# # ========== Add Brightness from Two Images ==========
# def add_image_brightness(img1, img2):
#     # Resize second image to match the first
#     h1, w1 = img1.shape[:2]
#     img2_resized = cv2.resize(img2, (w1, h1))

#     # Add pixel values
#     added = cv2.add(img1, img2_resized)

#     return added

# # ========== Resize Utility ==========
# def image_size(img, maxSize):
#     w, h = img.size
#     if w > h:
#         w, h = maxSize, int(h * (maxSize / img.width))
#     else:
#         h, w = maxSize, int(w * (maxSize / img.height))
#     return (w, h)

# # ========== App ==========
# app = ctk.CTk()
# app.geometry("900x600")
# app.title("Add Brightness from Two Images")

# image1 = None
# image2 = None

# # ========== Left Frame ==========
# left_frame = ctk.CTkFrame(app, width=200)
# left_frame.pack(side="left", fill="y", padx=10, pady=10)
# left_frame.pack_propagate(False)

# # ========== Right Frame ==========
# right_frame = ctk.CTkFrame(app)
# right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
# right_frame.pack_propagate(False)

# # ========== Upload First Image ==========
# def upload_image1():
#     global image1
#     path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
#     if path:
#         image1 = Image.open(path)
#         resized = image_size(image1, 300)
#         img_ctk = ctk.CTkImage(light_image=image1, size=resized)
#         img_label.configure(image=img_ctk, text="")
#         img_label.image = img_ctk

# # ========== Upload Second Image ==========
# def upload_image2():
#     global image2
#     path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
#     if path:
#         image2 = Image.open(path)
#         messagebox.showinfo("Success", "Second image uploaded.")

# # ========== Apply Combined Brightness ==========
# def combine_brightness():
#     global image1, image2
#     if image1 is None or image2 is None:
#         messagebox.showerror("Error", "Please upload both images first.")
#         return

#     try:
#         img1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
#         img2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)

#         result_cv = add_image_brightness(img1_cv, img2_cv)

#         result_pil = Image.fromarray(cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB))
#         result_ctk = ctk.CTkImage(light_image=result_pil, size=image_size(result_pil, 500))

#         result_label.configure(image=result_ctk, text="")
#         result_label.image = result_ctk

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # ========== Left Frame Buttons ==========
# upload_btn1 = ctk.CTkButton(left_frame, text="Upload First Image", command=upload_image1)
# upload_btn1.pack(pady=10)

# upload_btn2 = ctk.CTkButton(left_frame, text="Upload Second Image", command=upload_image2)
# upload_btn2.pack(pady=10)

# combine_btn = ctk.CTkButton(left_frame, text="Add Brightness", command=combine_brightness)
# combine_btn.pack(pady=10)

# img_label = ctk.CTkLabel(left_frame, text="No Image")
# img_label.pack(pady=20)

# # ========== Right Frame Output ==========
# result_label = ctk.CTkLabel(right_frame, text="Result will appear here")
# result_label.pack(pady=20)

# # ========== Mainloop ==========
# app.mainloop()


import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2

def image_size(img, maxSize):
    w, h = img.size
    if w > h:
        w, h = maxSize, int(h * (maxSize / img.width))
    else:
        h, w = maxSize, int(w * (maxSize / img.height))
    return (w, h)

def add_brightness_only(img1, img2):

    h1, w1 = img1.shape[:2]
    img2_resized = cv2.resize(img2, (w1, h1))


    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

    result_brightness = cv2.add(gray1, gray2)  

    return result_brightness

app = ctk.CTk()
app.geometry("900x600")
app.title("Combine Brightness Only")

image1 = None
image2 = None

left_frame = ctk.CTkFrame(app, width=200)
left_frame.pack(side="left", fill="y", padx=10, pady=10)
left_frame.pack_propagate(False)

right_frame = ctk.CTkFrame(app)
right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
right_frame.pack_propagate(False)


def upload_image1():
    global image1
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
    if path:
        image1 = Image.open(path)
        resized = image_size(image1, 300)
        img_ctk = ctk.CTkImage(light_image=image1, size=resized)
        img_label.configure(image=img_ctk, text="")
        img_label.image = img_ctk


def upload_image2():
    global image2
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
    if path:
        image2 = Image.open(path)
        messagebox.showinfo("Success", "Second image uploaded.")


def combine_brightness():
    global image1, image2
    if image1 is None or image2 is None:
        messagebox.showerror("Error", "Please upload both images.")
        return

    try:
        img1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
        img2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)

        result_brightness = add_brightness_only(img1_cv, img2_cv)

        result_pil = Image.fromarray(result_brightness)
        result_ctk = ctk.CTkImage(light_image=result_pil, size=image_size(result_pil, 500))

        result_label.configure(image=result_ctk, text="")
        result_label.image = result_ctk

    except Exception as e:
        messagebox.showerror("Error", str(e))

upload_btn1 = ctk.CTkButton(left_frame, text="Upload First Image", command=upload_image1)
upload_btn1.pack(pady=10)

upload_btn2 = ctk.CTkButton(left_frame, text="Upload Second Image", command=upload_image2)
upload_btn2.pack(pady=10)

combine_btn = ctk.CTkButton(left_frame, text="Add Brightness Only", command=combine_brightness)
combine_btn.pack(pady=10)

img_label = ctk.CTkLabel(left_frame, text="No Image")
img_label.pack(pady=20)

result_label = ctk.CTkLabel(right_frame, text="Result will appear here")
result_label.pack(pady=20)

app.mainloop()


