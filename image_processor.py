from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from customtkinter import filedialog
from functools import partial
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Import image processing functions
from image_processing_functions import add_brightness, subtract_brightness, divide_brightness, complement_image
from image_processing_functions import increase_red_channel, swap_red_green, remove_red_channel
from image_processing_functions import average_filter, laplacian_filter, maximum_filter, minimum_filter
from image_processing_functions import median_filter, mode_filter
from image_processing_functions import Rank_filter, Outlier_filter
from image_histogram import histogram_stretching, histogram_equalization, show_histogram


# Import new modules
import sys
import os
# sys.path.append(os.path.abspath("D:/DIP grok"))
import image_segmentation
import edge_detection
import morphological_operations

# Import destroy_and_restart function
from destroy_win import destroy_and_restart

# Initialize main window
root = ctk.CTk()
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
root.title('Image Processor')
root.geometry("900x600")

# Global variables
image_Pil = None
image = None
image_after_operatoin = None
upload_btn_img = None
multiple_images = []
image_path = None  # Added to store the path of the uploaded image

# ========================================= OPERATION FUNCTIONS =========================================

def Point_operation():
    for child in image_operations.winfo_children():
        child.destroy()

    frame = ctk.CTkFrame(image_operations)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    label = ctk.CTkLabel(frame, text="Choose a point operation", font=("Arial", 16))
    label.pack(pady=10)

    def apply_operation(choice):
        global image_Pil, image_after_operatoin
        if image_Pil is None:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        img_cv = cv2.cvtColor(np.array(image_Pil), cv2.COLOR_RGB2BGR)

        try:
            if choice == 1:
                processed = add_brightness(img_cv)
            elif choice == 2:
                processed = subtract_brightness(img_cv)
            elif choice == 3:
                processed = divide_brightness(img_cv)
            elif choice == 4:
                processed = complement_image(img_cv)
            else:
                raise ValueError("Invalid choice")

            processed_pil = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            image_after_operatoin = ctk.CTkImage(processed_pil, size=image_size(processed_pil, 500))

            for child in image_operations.winfo_children():
                child.destroy()
            img_label = ctk.CTkLabel(image_operations, image=image_after_operatoin, text="")
            img_label.pack(expand=True)

        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to apply operation: {str(e)}")

    ops = [
        ("Add Brightness", 1),
        ("Subtract Brightness", 2),
        ("Divide Brightness", 3),
        ("Complement Image", 4)
    ]

    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Point Operations", [lambda v=val: apply_operation(v) for op, val in ops])

def Color_image_operation():
    global image_Pil, image_after_operatoin

    if image_Pil is None:
        messagebox.showinfo("Error", "Please upload an image first.")
        return

    for widget in image_operations.winfo_children():
        widget.destroy()

    def apply_operation(choice):
        global image_Pil, image_after_operatoin
        try:
            img_cv = cv2.cvtColor(np.array(image_Pil), cv2.COLOR_RGB2BGR)

            if choice == 1:
                result = increase_red_channel(img_cv)
            elif choice == 2:
                result = swap_red_green(img_cv)
            elif choice == 3:
                result = remove_red_channel(img_cv)
            else:
                messagebox.showerror("Error", "Invalid choice.")
                return

            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            image_Pil_after = Image.fromarray(result_rgb)
            image_after_operatoin = ctk.CTkImage(image_Pil_after, size=image_size(image_Pil_after, 500))

            for child in image_operations.winfo_children():
                child.destroy()
            label_center = ctk.CTkLabel(image_operations, text="", image=image_after_operatoin)
            label_center.pack(expand=True)
        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to apply color operation: {str(e)}")

    ops = [
        ("Increase Red Channel", 1),
        ("Swap Red and Green", 2),
        ("Remove Red Channel", 3)
    ]

    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Color Operations", [lambda v=val: apply_operation(v) for op, val in ops])

def Image_Histogram():
    global image_Pil, image_after_operatoin

    if image_Pil is None:
        messagebox.showinfo("Error", "Please upload an image first.")
        return

    for widget in image_operations.winfo_children():
        widget.destroy()

    def apply_operation(choice):
        global image_Pil, image_after_operatoin
        try:
            img_cv = cv2.cvtColor(np.array(image_Pil), cv2.COLOR_RGB2BGR)
            
            if choice == 1:
                processed = histogram_stretching(img_cv)
            elif choice == 2:
                processed = histogram_equalization(img_cv)
            elif choice == 3:
                hist_img = show_histogram(img_cv)
                hist_ctk_img = ctk.CTkImage(hist_img, size=image_size(hist_img, 500))
                for child in image_operations.winfo_children():
                    child.destroy()
                img_label = ctk.CTkLabel(image_operations, image=hist_ctk_img, text="")
                img_label.pack(expand=True)
                return
            else:
                raise ValueError("Invalid choice")

            processed_pil = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            image_after_operatoin = ctk.CTkImage(processed_pil, size=image_size(processed_pil, 500))

            for child in image_operations.winfo_children():
                child.destroy()
            img_label = ctk.CTkLabel(image_operations, image=image_after_operatoin, text="")
            img_label.pack(expand=True)
            
        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to apply histogram operation: {str(e)}")

    ops = [
        ("Histogram Stretching", 1),
        ("Histogram Equalization", 2),
        ("Show Histogram", 3)
    ]

    buttons([op[0] for op in ops], "Histogram Operations", [lambda v=val: apply_operation(v) for op, val in ops])


def Neighborhood_Processing():
    global image_Pil, image_after_operatoin

    if image_Pil is None:
        messagebox.showinfo("Error", "Please upload an image first.")
        return

    for widget in image_operations.winfo_children():
        widget.destroy()

    def apply_operation(operation):
        global image_Pil, image_after_operatoin
        try:
            img_cv = cv2.cvtColor(np.array(image_Pil), cv2.COLOR_RGB2BGR)
            
            if operation == 1:
                processed = average_filter(img_cv)
            elif operation == 2:
                processed = laplacian_filter(img_cv)
            elif operation == 3:
                processed = maximum_filter(img_cv)
            elif operation == 4:
                processed = minimum_filter(img_cv)
            elif operation == 5:
                processed = median_filter(img_cv)
            elif operation == 6:
                processed = mode_filter(img_cv)
            else:
                raise ValueError("Invalid operation")
            
            processed_pil = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            image_after_operatoin = ctk.CTkImage(processed_pil, size=image_size(processed_pil, 500))
            
            for child in image_operations.winfo_children():
                child.destroy()
            img_label = ctk.CTkLabel(image_operations, image=image_after_operatoin, text="")
            img_label.pack(expand=True)
        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to apply {operation} filter: {str(e)}")

    ops = [
        ("Average Filter", 1),
        ("Laplacian Filter", 2),
        ("Maximum Filter", 3),
        ("Minimum Filter", 4),
        ("Median Filter", 5),
        ("Mode Filter", 6)
    ]

    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Neighborhood Operations", [lambda v=val: apply_operation(v) for op, val in ops])

def Image_Restoration():
    global image_Pil, image_after_operatoin, multiple_images

    if image_Pil is None:
        messagebox.showinfo("Error", "Please upload an image first.")
        return

    for widget in image_operations.winfo_children():
        widget.destroy()

    def apply_operation(choice):
        global image_Pil, image_after_operatoin, multiple_images
        try:
            img_cv = cv2.cvtColor(np.array(image_Pil), cv2.COLOR_RGB2BGR)
            
            if choice == 1:  # Average Filter
                processed = average_filter(img_cv)
            elif choice == 2:  # Median Filter
                processed = median_filter(img_cv)
            elif choice == 3:  # Rank Filter
                processed = Rank_filter(img_cv, 4)  # Default rank value
            elif choice == 4:  # Outlier Filter
                processed = Outlier_filter(img_cv, 40)  # Default threshold value
            elif choice == 5:  # Upload Images for Averaging
                files = filedialog.askopenfilenames(
                    filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
                )
                if files:
                    multiple_images.clear()  # Clear previous selections
                    for file in files:
                        if os.path.exists(file):
                            multiple_images.append(file)
                        else:
                            messagebox.showwarning("Warning", f"File not found: {file}")
                    if multiple_images:
                        messagebox.showinfo("Success", f"{len(multiple_images)} valid images selected for averaging")
                    else:
                        messagebox.showwarning("Warning", "No valid images were selected")
                return
            elif choice == 6:  # Apply Image Averaging
                if not multiple_images:
                    messagebox.showerror("Error", "Please select images for averaging first")
                    return
                if len(multiple_images) < 2:
                    messagebox.showerror("Error", "Please select at least 2 images for averaging")
                    return
                
                # Read all images
                images = []
                for path in multiple_images:
                    img = cv2.imread(path)
                    if img is None:
                        messagebox.showwarning("Warning", f"Failed to load image: {path}")
                        continue
                    images.append(img)
                
                if len(images) < 2:
                    messagebox.showerror("Error", "Not enough valid images for averaging")
                    return
                
                # Ensure all images have the same dimensions and channels
                base_height, base_width = images[0].shape[:2]
                base_channels = images[0].shape[2] if len(images[0].shape) > 2 else 1
                processed_images = []
                
                for img in images:
                    if img.shape[:2] != (base_height, base_width):
                        img = cv2.resize(img, (base_width, base_height))
                    if len(img.shape) == 2 and base_channels == 3:
                        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                    elif len(img.shape) == 3 and base_channels == 1:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    processed_images.append(img.astype(np.float32))
                
                # Perform averaging
                processed = np.zeros_like(processed_images[0])
                for img in processed_images:
                    processed += img
                processed = np.clip(processed / len(processed_images), 0, 255).astype(np.uint8)
            else:
                raise ValueError("Invalid choice")

            if choice != 5:  # Don't update display for upload operation
                if len(processed.shape) == 2:
                    processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
                processed_pil = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
                image_after_operatoin = ctk.CTkImage(processed_pil, size=image_size(processed_pil, 500))
                
                for child in image_operations.winfo_children():
                    child.destroy()
                img_label = ctk.CTkLabel(image_operations, image=image_after_operatoin, text="")
                img_label.pack(expand=True)
                
        except Exception as e:
            messagebox.showerror("Processing Error", f"Failed to apply restoration operation: {str(e)}")

    ops = [
        ("Average Filter", 1),
        ("Median Filter", 2),
        ("Rank Filter", 3),
        ("Outlier Filter", 4),
        ("Upload Images for Averaging", 5),
        ("Apply Image Averaging", 6)
    ]

    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Restoration Operations", [lambda v=val: apply_operation(v) for op, val in ops])

def Image_Segmentation():
    global image_Pil, image_path
    if image_Pil is None or image_path is None:
        messagebox.showinfo("Info", "Please upload an image first.")
        return
    
    for child in image_operations.winfo_children():
        child.destroy()

    def apply_operation(choice):
        try:
            img_cv = cv2.imread(image_path)
            
            if choice == 1:  # Basic Thresholding
                result = image_segmentation.basic_thresholding(img_cv)
            elif choice == 2:  # Automatic Iterative Thresholding
                _, result = image_segmentation.automatic_threshold_iterative(img_cv)
            elif choice == 3:  # Adaptive Thresholding by Rows
                result = image_segmentation.Adaptive_Thresholding_The_Chow_and_Kaneko_approach_by_rows(img_cv)
            elif choice == 4:  # Region-Based Clustering
                clustered = image_segmentation.region_based_clustering(img_cv)
                # Convert cluster labels to grayscale image for visualization
                norm_cluster = cv2.normalize(clustered.astype('float'), None, 0, 255, cv2.NORM_MINMAX)
                result = norm_cluster.astype(np.uint8)
            else:
                messagebox.showerror("Error", "Unknown operation.")
                return
            
            # Save result temporarily
            save_path = "segmentation_results/{}_result.png".format(ops[choice-1][0].replace(" ", "_").lower())
            os.makedirs("segmentation_results", exist_ok=True)
            cv2.imwrite(save_path, result)

            # Show result in GUI
            for child in image_operations.winfo_children():
                child.destroy()
            result_img = Image.open(save_path)
            result_ctk_img = ctk.CTkImage(result_img, size=image_size(result_img, 500))
            lbl = ctk.CTkLabel(image_operations, text=ops[choice-1][0], font=("Arial", 18))
            lbl.pack(pady=8)
            img_lbl = ctk.CTkLabel(image_operations, image=result_ctk_img, text="")
            img_lbl.image = result_ctk_img
            img_lbl.pack()
            
        except Exception as e:
            messagebox.showerror("Error", f"Segmentation failed: {e}")

    ops = [
        ("Basic Thresholding", 1),
        ("Automatic Iterative Thresholding", 2),
        ("Adaptive Thresholding by Rows", 3),
        ("Region-Based Clustering", 4)
    ]
    
    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Segmentation Operations", [lambda v=val: apply_operation(v) for op, val in ops])

def Edge_Detection():
    global image_Pil, image_path
    if image_Pil is None or image_path is None:
        messagebox.showinfo("Info", "Please upload an image first.")
        return

    for child in image_operations.winfo_children():
        child.destroy()

    def apply_operation(choice):
        try:
            if choice == 1:  # Sobel Edge Detection
                result_path = edge_detection.sobel_filter(image_path)
                
                if os.path.exists(result_path):
                    result_img = Image.open(result_path)
                    result_ctk_img = ctk.CTkImage(result_img, size=image_size(result_img, 500))
                    lbl = ctk.CTkLabel(image_operations, text="Sobel Edge Detection", font=("Arial", 18))
                    lbl.pack(pady=8)
                    img_lbl = ctk.CTkLabel(image_operations, image=result_ctk_img, text="")
                    img_lbl.image = result_ctk_img
                    img_lbl.pack()
                else:
                    messagebox.showerror("Error", "Failed to generate edge detection image.")
            else:
                messagebox.showerror("Error", "Unknown operation.")

        except Exception as e:
            messagebox.showerror("Error", f"Edge detection failed: {e}")

    ops = [
        ("Sobel Edge Detection", 1)
    ]
    
    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Edge Detection Operations", [lambda v=val: apply_operation(v) for op, val in ops])

def Mathematical_Morphology():
    global image_Pil, image_path
    if image_Pil is None or image_path is None:
        messagebox.showinfo("Info", "Please upload an image first.")
        return

    for child in image_operations.winfo_children():
        child.destroy()

    def apply_operation(choice):
        try:
            if choice == 1:  # Dilation
                morphological_operations.dilation(image_path)
                result_path = "morphology_images/dilation.jpg"
            elif choice == 2:  # Erosion
                morphological_operations.erosion(image_path)
                result_path = "morphology_images/erosion.jpg"
            elif choice == 3:  # Opening
                morphological_operations.opening(image_path)
                result_path = "morphology_images/opening.jpg"
            elif choice == 4:  # Internal Boundary
                morphological_operations.internal_boundary(image_path)
                result_path = "morphology_images/internal_boundary.jpg"
            elif choice == 5:  # External Boundary
                morphological_operations.external_boundary(image_path)
                result_path = "morphology_images/external_boundary.jpg"
            elif choice == 6:  # Morphological Gradient
                morphological_operations.morph_gradient(image_path)
                result_path = "morphology_images/morph_gradient.jpg"
            else:
                messagebox.showerror("Error", "Unknown operation.")
                return

            if os.path.exists(result_path):
                for child in image_operations.winfo_children():
                    child.destroy()
                result_img = Image.open(result_path)
                result_ctk_img = ctk.CTkImage(result_img, size=image_size(result_img, 500))
                lbl = ctk.CTkLabel(image_operations, text=ops[choice-1][0], font=("Arial", 18))
                lbl.pack(pady=8)
                img_lbl = ctk.CTkLabel(image_operations, image=result_ctk_img, text="")
                img_lbl.image = result_ctk_img
                img_lbl.pack()
            else:
                messagebox.showerror("Error", "Failed to generate morphological operation image.")
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {e}")

    ops = [
        ("Dilation", 1),
        ("Erosion", 2),
        ("Opening", 3),
        ("Internal Boundary", 4),
        ("External Boundary", 5),
        ("Morphological Gradient", 6)
    ]
    
    # Update the buttons in the left panel
    buttons([op[0] for op in ops], "Morphological Operations", [lambda v=val: apply_operation(v) for op, val in ops])


# =======================================================================================================
def apply_vertical_segmentation(threshold=45, min_segment_height=5):
    global image_Pil
    
    if image_Pil is None:
        messagebox.showerror("Error", "Please upload an image first")
        return None
    
    try:
        img = np.array(image_Pil)
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        h, w = img.shape
        result = np.zeros_like(img, dtype=np.uint8)
        cluster_id = 1
        
        for j in range(w):
            current_val = img[0, j]
            segment_start = 0
            
            for i in range(1, h):
                if abs(int(img[i, j]) - int(current_val)) > threshold:
                    if (i - segment_start) >= min_segment_height:
                        result[segment_start:i, j] = cluster_id
                        cluster_id = min(cluster_id + 25, 255)
                        segment_start = i
                        current_val = img[i, j]
            
            if (h - segment_start) >= min_segment_height:
                result[segment_start:h, j] = cluster_id
        
        if cluster_id > 1:
            result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)
        
        return Image.fromarray(result)
    
    except Exception as e:
        messagebox.showerror("Processing Error", str(e))
        return None

# ========================================= MAIN PAGE FUNCTIONS =========================================

def upload():
    global image_Pil, image, image_after_operatoin, image_path
    try:
        uploaded_file = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
        )
        if uploaded_file and os.path.exists(uploaded_file):
            image_Pil = Image.open(uploaded_file)
            image_path = uploaded_file
            image = ctk.CTkImage(image_Pil, size=image_size(image_Pil, 200))
            img_container.configure(image=image, text="")
            for child in image_operations.winfo_children():
                child.destroy()
            image_after_operatoin = ctk.CTkImage(image_Pil, size=image_size(image_Pil, 500))
            label_center = ctk.CTkLabel(image_operations, text="", image=image_after_operatoin)
            label_center.pack(expand=True)
            buttons(combo_defs, "Image Operations", functions)
    except Exception as e:
        messagebox.showinfo("Error", f"An error occurred while uploading: {str(e)}")
        return

def image_size(img, maxSize):
    original_width, original_height = img.size
    w = original_width
    h = original_height
    if original_width > original_height:
        original_width /= w / maxSize
        original_height /= w / maxSize
    else:
        original_width /= h / maxSize
        original_height /= h / maxSize 
    return (int(original_width), int(original_height))

def reupload(e=None):
    """Handle reupload button click by restarting the application."""
    destroy_and_restart(root)

def initialization(parent_frame):
    global upload_btn, upload_btn_img
    try:
        if not os.path.exists("images/arithmatic_operations.png"):
            raise FileNotFoundError("Image not found: images/arithmatic_operations.png")

        img_pil = Image.open("images/arithmatic_operations.png")
        upload_btn_img = ctk.CTkImage(light_image=img_pil, size=image_size(img_pil, 200))

        frame1 = ctk.CTkFrame(parent_frame, fg_color='transparent')
        frame1.pack(expand=True)

        upload_btn = ctk.CTkButton(
            frame1,
            height=100,
            width=100,
            text="",
            fg_color="transparent",
            hover=False,
            image=upload_btn_img,
            command=upload
        )
        upload_btn.pack()
        vertical_seg_btn = ctk.CTkButton(frame1, text="Vertical Segmentation", command=apply_vertical_segmentation)
        vertical_seg_btn.pack(pady=10)
        combo_defs.append("Vertical Segmentation")
        functions.append(apply_vertical_segmentation)

    except Exception as e:
        messagebox.showerror("Initialization Error", f"Failed to load image: {str(e)}")

# Operation definitions
combo_defs = [
    "Point operation",
    "Color image operation",
    "Image Histogram",
    "Neighborhood Processing",
    "Image Restoration",
    "Image Segmentation",
    "Edge Detection",
    "Mathematical Morphology"
]

functions = [
    Point_operation,
    Color_image_operation,
    Image_Histogram,
    Neighborhood_Processing,
    Image_Restoration,
    Image_Segmentation,
    Edge_Detection,
    Mathematical_Morphology
]

def back_to_main():
    # Clear the image operations area
    for child in image_operations.winfo_children():
        child.destroy()
    # Show the original image if it exists
    if image_after_operatoin:
        label_center = ctk.CTkLabel(image_operations, text="", image=image_after_operatoin)
        label_center.pack(expand=True)
    # Restore main operation buttons
    buttons(combo_defs, "Image operations", functions)

def buttons(btn_titles, text, func):
    for child in btn_frame.winfo_children():
        child.destroy()
    label2 = ctk.CTkLabel(btn_frame, text=text, font=("Arial", 16))
    label2.pack()
    
    # Add back button if not in main menu
    if btn_titles != combo_defs:
        back_btn = ctk.CTkButton(btn_frame, text="Back to Main Menu", width=180, command=back_to_main)
        back_btn.pack(pady=6)
    
    for title, i in zip(btn_titles, func):
        cb = ctk.CTkButton(btn_frame, text=title, width=180, command=i)
        cb.pack(pady=6)

# ========================================= UI LAYOUT =========================================

# Control section (left panel)
control_section = ctk.CTkFrame(root, width=250)
control_section.pack(fill='y', side='left', ipadx=5, ipady=5)
control_section.pack_propagate(False)

# Original image display
original_img = ctk.CTkFrame(control_section, height=200)
original_img.pack(side='top', fill='x')
original_img.pack_propagate(False)

label1 = ctk.CTkLabel(original_img, text="Original Image", font=("Arial", 16))
label1.pack()
img_container = ctk.CTkLabel(original_img, text="")
img_container.pack()

# Add a frame for the reupload button
reupload_frame = ctk.CTkFrame(control_section)
reupload_frame.pack(side='top', fill='x', pady=5)

# Add the "Clear & Upload New Image" button
reupload_btn = ctk.CTkButton(
    reupload_frame,
    text="Clear & Upload New Image",
    width=180,
    command=reupload
)
reupload_btn.pack()

# Operation buttons
btn_frame = ctk.CTkScrollableFrame(control_section)
btn_frame.pack(side='top', fill='both', expand=True, ipadx=5, ipady=5, pady=5)
buttons(combo_defs, "Image operations", functions)

# Image operations display (main area)
image_operations = ctk.CTkFrame(root)
image_operations.pack(fill='both', expand=True, padx=15, pady=15)

# Initialize with empty operation screen and upload button
initialization(image_operations)

# Bind reupload on key press
root.bind("<Key>", reupload)

root.mainloop()

