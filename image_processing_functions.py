import cv2
import numpy as np
from scipy import stats

# ========================================= IMAGE PROCESSING FUNCTIONS =========================================

# Brightness operations
def add_brightness(img, value=50):
    modified = img.copy()
    if len(modified.shape) == 2:  # Grayscale
        modified = cv2.add(modified, value)
    elif len(modified.shape) == 3 and modified.shape[2] == 3:  # Color
        modified = cv2.add(modified, np.array([value, value, value]))
    else:
        raise ValueError("Unsupported image format")
    return modified

def subtract_brightness(img, value=50):
    modified = img.copy()
    if len(modified.shape) == 2:
        modified = cv2.subtract(modified, value)
    elif len(modified.shape) == 3 and modified.shape[2] == 3:
        modified = cv2.subtract(modified, np.array([value, value, value]))
    else:
        raise ValueError("Unsupported image format")
    return modified

def divide_brightness(img, divisor=2.0):
    modified = img.copy().astype(np.float32)
    if len(modified.shape) == 2:
        modified = modified / divisor
    elif len(modified.shape) == 3 and modified.shape[2] == 3:
        modified = modified / np.array([divisor, divisor, divisor])
    else:
        raise ValueError("Unsupported image format")
    return np.clip(modified, 0, 255).astype(np.uint8)

def complement_image(img):
    if len(img.shape) not in [2, 3]:
        raise ValueError("Unsupported image format")
    return cv2.bitwise_not(img)


def Point_operation():
    global image_Pil, image_after_operatoin

    if image_Pil is None:
        messagebox.showinfo("Error", "Please upload an image first.")
        return

    for widget in image_operations.winfo_children():
        widget.destroy()

    # Popup to choose operation and value
    def open_popup():
        popup = ctk.CTkToplevel()
        popup.title("Point Operation")
        popup.geometry("300x200")

        label = ctk.CTkLabel(popup, text="Select Operation:")
        label.pack(pady=5)

        options = ["Add Brightness", "Subtract Brightness", "Divide Brightness", "Complement Image"]
        op_menu = ctk.CTkOptionMenu(popup, values=options)
        op_menu.pack(pady=5)

        value_label = ctk.CTkLabel(popup, text="Enter Value:")
        value_label.pack(pady=5)
        value_entry = ctk.CTkEntry(popup)
        value_entry.pack(pady=5)

        def apply():
            try:
                choice = op_menu.get()
                val_text = value_entry.get()
                val = int(val_text) if val_text else 50  # default if empty

                img_cv = cv2.cvtColor(np.array(image_Pil), cv2.COLOR_RGB2BGR)

                if choice == "Add Brightness":
                    result = add_brightness(img_cv, val)
                elif choice == "Subtract Brightness":
                    result = subtract_brightness(img_cv, val)
                elif choice == "Divide Brightness":
                    result = divide_brightness(img_cv, divisor=val)
                elif choice == "Complement Image":
                    result = complement_image(img_cv)
                else:
                    messagebox.showerror("Error", "Unknown operation")
                    return

                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                processed_pil = Image.fromarray(result_rgb)
                image_after_operatoin = ctk.CTkImage(processed_pil, size=image_size(processed_pil, 500))

                for child in image_operations.winfo_children():
                    child.destroy()
                label_center = ctk.CTkLabel(image_operations, image=image_after_operatoin, text="")
                label_center.pack(expand=True)
                popup.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply operation: {str(e)}")

        apply_btn = ctk.CTkButton(popup, text="Apply", command=apply)
        apply_btn.pack(pady=10)

    # Show the popup
    open_popup()


# Color operations
def increase_red_channel(img, value=50):
    modified = np.array(img).copy()
    if len(modified.shape) == 2:  # Grayscale image
        modified = np.clip(modified + value, 0, 255)
    elif len(modified.shape) == 3 and modified.shape[2] == 3:  # Color image
        modified[:, :, 2] = np.clip(modified[:, :, 2] + value, 0, 255)
    else:
        raise ValueError("Unsupported image format")
    return modified.astype(np.uint8)

def swap_red_green(img):
    if len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError("Swapping red and green only works on color images")
    swapped = img.copy()
    swapped[:, :, 1], swapped[:, :, 2] = swapped[:, :, 2].copy(), swapped[:, :, 1].copy()
    return swapped

def remove_red_channel(img):
    modified = img.copy()
    if len(modified.shape) == 2:  # Grayscale
        modified[:, :] = 0
    elif len(modified.shape) == 3 and modified.shape[2] == 3:
        modified[:, :, 2] = 0  # Remove red channel
    else:
        raise ValueError("Unsupported image format")
    return modified

# Neighborhood Processing operations
def _apply_kernel_gray(img, kernel):
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+kh, j:j+kw]
            output[i, j] = np.clip(np.sum(region * kernel), 0, 255)
    return output

def apply_kernel(img, kernel):
    if len(img.shape) == 2:  # Grayscale
        return _apply_kernel_gray(img, kernel)
    elif len(img.shape) == 3:  # Color
        channels = cv2.split(img)
        filtered_channels = [_apply_kernel_gray(c, kernel) for c in channels]
        return cv2.merge(filtered_channels)
    else:
        raise ValueError("Unsupported image format")

def average_filter(img, size=3):
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    return apply_kernel(img, kernel)

def laplacian_filter(img):
    kernel = np.array([[0, 1, 0],
                      [1, -4, 1],
                      [0, 1, 0]])
    return apply_kernel(img, kernel)

def _nonlinear_filter_gray(img, size, func):
    pad = size // 2
    padded = np.pad(img, pad, mode='reflect')
    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+size, j:j+size]
            output[i, j] = func(region)
    return output

def _apply_nonlinear_filter(img, size, func):
    if len(img.shape) == 2:
        return _nonlinear_filter_gray(img, size, func)
    elif len(img.shape) == 3:
        channels = cv2.split(img)
        filtered_channels = [_nonlinear_filter_gray(c, size, func) for c in channels]
        return cv2.merge(filtered_channels)
    else:
        raise ValueError("Unsupported image format")

def maximum_filter(img, size=3):
    return _apply_nonlinear_filter(img, size, np.max)

def minimum_filter(img, size=3):
    return _apply_nonlinear_filter(img, size, np.min)

def median_filter(img, size=3):
    return _apply_nonlinear_filter(img, size, np.median)

def mode_filter(img, size=3):
    def mode_func(region):
        flat_region = region.astype(int).flatten()
        values, counts = np.unique(flat_region, return_counts=True)
        if len(values) == 0:
            return 0
        return values[np.argmax(counts)]
    return _apply_nonlinear_filter(img, size, mode_func)

#  Restoration operations


def Rank_filter(image, rank=4):
    img_bgr = image
    if len(img_bgr.shape) == 2:
        img = img_bgr
    else:
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    if len(img.shape) == 2:
        padded_img = np.pad(img, 1, mode='reflect')
        new_img = np.zeros_like(img)
        for i in range(1, img.shape[0] + 1):
            for j in range(1, img.shape[1] + 1):
                region = padded_img[i - 1:i + 2, j - 1:j + 2].flatten()
                sorted_vals = np.sort(region)
                rank_val = sorted_vals[min(rank, len(sorted_vals) - 1)]
                new_img[i - 1, j - 1] = np.uint8(rank_val)
    else:
        h, w, ch = img.shape
        new_img = np.zeros_like(img)
        padded_img = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode='reflect')
        for i in range(1, h + 1):
            for j in range(1, w + 1):
                for c in range(ch):
                    region = padded_img[i - 1:i + 2, j - 1:j + 2, c].flatten()
                    sorted_vals = np.sort(region)
                    rank_val = sorted_vals[min(rank, len(sorted_vals) - 1)]
                    new_img[i - 1, j - 1, c] = np.uint8(rank_val)

    return new_img

def Outlier_filter(image, threshold=40):
    img_bgr = image
    if len(img_bgr.shape) == 2:
        img = img_bgr
    else:
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    new_img = np.copy(img)
    if len(img.shape) == 2:
        padded_img = np.pad(img, 1, mode='reflect')
        for i in range(1, img.shape[0] + 1):
            for j in range(1, img.shape[1] + 1):
                region = padded_img[i - 1:i + 2, j - 1:j + 2].flatten()
                center = region[4]
                neighbors = np.delete(region, 4)
                mean = np.mean(neighbors)
                new_img[i - 1, j - 1] = np.uint8(mean if abs(int(center) - mean) > threshold else center)
    else:
        h, w, ch = img.shape
        padded_img = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode='reflect')
        for i in range(1, h + 1):
            for j in range(1, w + 1):
                for c in range(ch):
                    region = padded_img[i - 1:i + 2, j - 1:j + 2, c].flatten()
                    center = region[4]
                    neighbors = np.delete(region, 4)
                    mean = np.mean(neighbors)
                    new_val = mean if abs(int(center) - mean) > threshold else center
                    new_img[i - 1, j - 1, c] = np.uint8(new_val)

    return new_img



# Restoration operations

# def rank_func(region, rank=4):
#     sorted_vals = np.sort(region)
#     return sorted_vals[min(rank, len(sorted_vals) - 1)]


# def rank_filter(img, size=3, rank=4):
#     def func(region):
#         return rank_func(region, rank)
#     return _apply_nonlinear_filter(img, size, func)


# def outlier_func(region, threshold=40):
#     center = region[len(region)//2]
#     neighbors = np.delete(region, len(region)//2)
#     mean = np.mean(neighbors)
#     return mean if abs(int(center) - mean) > threshold else center


# def outlier_filter(img, size=3, threshold=40):
#     def func(region):
#         return outlier_func(region, threshold)
#     return _apply_nonlinear_filter(img, size, func)