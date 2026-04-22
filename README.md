# 🖼️ Digital Image Processing Toolbox — DIP v2.5

A feature-rich **desktop application** for Digital Image Processing built with Python and CustomTkinter. It provides an interactive GUI for applying a wide range of image processing operations — from basic point operations to advanced morphological transformations.

---

## 👥 Team Members

| Name | Role |
|---|---|
| **Mohamed Elhadad** | Developer |
| **Ahmed Shamh** | Developer |
| **Mohamed Elfiky** | Developer |
| **Hagar Ayman** | Developer |
| **Huda Mahmoud** | Developer |

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Operations Reference](#operations-reference)

---

## Overview

DIP v2.5 is a university project developed for the **Digital Image Processing** course. It allows users to upload any image and apply a comprehensive set of DIP operations through an intuitive graphical interface — no command-line interaction required.

The application is built on top of **OpenCV**, **NumPy**, **Matplotlib**, and **CustomTkinter**, combining classical DIP theory with a modern desktop UI.

---

## ✨ Features

- 📂 **Image Upload & Preview** — Load any JPG, PNG, BMP, TIFF, or GIF image
- 🔁 **Clear & Reload** — Restart the session and upload a new image instantly
- ↩️ **Back Navigation** — Return to the main menu from any sub-operation
- 🌗 **System Theme Support** — Automatically adapts to light/dark mode
- 📊 **Histogram Visualization** — Displays per-channel color histograms using Matplotlib
- 🖼️ **Multi-Image Support** — Upload multiple images for averaging/restoration workflows

---

## 🗂️ Project Structure

```
DIP_V2.5/
│
├── image_processor.py            # Main application entry point & GUI layout
├── image_processing_functions.py # Point, color, neighborhood & restoration ops
├── image_histogram.py            # Histogram stretching, equalization & display
├── image_segmentation.py         # Thresholding & region-based segmentation
├── edge_detection.py             # Sobel edge detection
├── morphological_operations.py   # Dilation, erosion, boundary & gradient ops
├── create_images.py              # Utility: generates noisy image variants
├── destroy_win.py                # Utility: window reset & app restart handler
│
├── images/                       # App assets & sample images
├── noise_images/                 # Output directory for noisy images
├── edge_images/                  # Output directory for edge detection results
├── morphology_images/            # Output directory for morphological results
├── segmentation_results/         # Output directory for segmentation results
└── histogram_results/            # Output directory for histogram plots
```

---

## 🧰 Requirements

- Python **3.8+**
- Libraries:

```
opencv-python
numpy
Pillow
matplotlib
customtkinter
scipy
```

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/mohamed-ibrahim09/DIP_V2.5--finall-.git
cd DIP_V2.5--finall-
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install opencv-python numpy Pillow matplotlib customtkinter scipy
```

**4. Run the application**

```bash
python image_processor.py
```

---

## 🚀 Usage

1. Launch the app with `python image_processor.py`
2. Click the **upload icon** in the center panel to load an image
3. Select an operation category from the left sidebar
4. Choose a specific operation — the result renders instantly in the main panel
5. Use **Back to Main Menu** to switch between operation categories
6. Use **Clear & Upload New Image** to reset and start fresh

---

## 🔬 Operations Reference

### 🔆 Point Operations
| Operation | Description |
|---|---|
| Add Brightness | Increases pixel intensity by a fixed value |
| Subtract Brightness | Decreases pixel intensity by a fixed value |
| Divide Brightness | Reduces contrast by dividing pixel values |
| Complement Image | Inverts all pixel values (`255 - pixel`) |

---

### 🎨 Color Image Operations
| Operation | Description |
|---|---|
| Increase Red Channel | Boosts the red channel intensity |
| Swap Red and Green | Swaps the R and G channels |
| Remove Red Channel | Zeroes out the red channel |

---

### 📊 Histogram Operations
| Operation | Description |
|---|---|
| Histogram Stretching | Expands pixel range to full [0, 255] using min-max scaling |
| Histogram Equalization | Redistributes intensities for improved contrast |
| Show Histogram | Plots per-channel frequency distribution |

---

### 🔲 Neighborhood Processing (Spatial Filtering)
| Filter | Type | Description |
|---|---|---|
| Average Filter | Linear | Blurs image using a mean kernel |
| Laplacian Filter | Linear | Sharpens edges via second-order derivatives |
| Maximum Filter | Non-linear | Replaces each pixel with the local max |
| Minimum Filter | Non-linear | Replaces each pixel with the local min |
| Median Filter | Non-linear | Removes salt-and-pepper noise |
| Mode Filter | Non-linear | Replaces pixel with the most frequent value in neighborhood |

---

### 🛠️ Image Restoration
| Operation | Description |
|---|---|
| Average Filter | Smoothing for noise reduction |
| Median Filter | Robust noise removal |
| Rank Filter | Selects the k-th sorted value in a neighborhood (default rank=4) |
| Outlier Filter | Replaces pixels deviating from the local mean beyond a threshold |
| Image Averaging | Averages multiple uploaded noisy images to reduce random noise |

---

### ✂️ Image Segmentation
| Method | Description |
|---|---|
| Basic Thresholding | Global binary threshold at pixel value 127 |
| Automatic Iterative Thresholding | Iteratively computes optimal threshold via mean convergence |
| Adaptive Thresholding (Chow-Kaneko) | Splits image into horizontal slices, applies Otsu per slice |
| Region-Based Clustering | Groups pixels into clusters based on intensity similarity |
| Vertical Segmentation | Column-wise segmentation based on intensity change thresholds |

---

### 🔍 Edge Detection
| Method | Description |
|---|---|
| Sobel Edge Detection | Computes gradient magnitude using Sobel X and Y kernels |

---

### 🔷 Mathematical Morphology
| Operation | Description |
|---|---|
| Dilation | Expands bright regions using a 5×5 structuring element |
| Erosion | Shrinks bright regions using a 5×5 structuring element |
| Opening | Erosion followed by dilation — removes small noise |
| Internal Boundary | `Original - Erosion` — extracts inner object edges |
| External Boundary | `Dilation - Original` — extracts outer object edges |
| Morphological Gradient | `Dilation - Erosion` — highlights full object boundaries |

---

## 📝 Notes

- All output images are automatically saved in their respective output directories (`edge_images/`, `morphology_images/`, `segmentation_results/`, `histogram_results/`)
- The application supports both **grayscale and color** images across all operations
- For **Image Averaging**, select at least 2 noisy images; the app will resize and align them automatically before averaging

---

## 📄 License

This project was developed for academic purposes as part of the **Digital Image Processing** course.

---

> Built with ❤️ by the DIP v2.5 Team — Menofia University
