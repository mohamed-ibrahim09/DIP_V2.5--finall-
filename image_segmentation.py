import numpy as np
import cv2

def basic_thresholding(img, thresh=127):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return np.where(img >= thresh, 255, 0).astype(np.uint8)

def automatic_threshold_iterative(img, tol=0.5, max_iter=100):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    Theta = img.mean()
    for _ in range(max_iter):
        p1 = img[img >= Theta]
        p2 = img[img < Theta]
        m1 = p1.mean() if p1.size > 0 else 0.0
        m2 = p2.mean() if p2.size > 0 else 0.0
        Theta_next = 0.5 * (m1 + m2)
        if abs(Theta_next - Theta) < tol:
            Theta = Theta_next
            break
        Theta = Theta_next

    _, binary = cv2.threshold(img, Theta, 255, cv2.THRESH_BINARY)
    return Theta, binary

def Adaptive_Thresholding_The_Chow_and_Kaneko_approach_by_rows(img, num_slices=4):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape
    slice_height = h // num_slices
    slices = [img[i * slice_height : h if i == num_slices - 1 else (i + 1) * slice_height, :] for i in range(num_slices)]

    binary_slices = []
    for sl in slices:
        _, th = cv2.threshold(sl, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_slices.append(th)

    binary = np.vstack(binary_slices)
    return binary

def region_based_clustering(img, threshold=45, min_cluster_size=4):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape
    clustered_img = np.zeros_like(img, dtype=int)
    clusters = []
    cluster_id = 1

    # Initialize first cluster
    clusters.append({'mean': img[0, 0], 'pixels': [(0, 0)], 'size': 1})
    clustered_img[0, 0] = cluster_id

    def add_pixel_to_cluster(cluster, pixel_value, coord):
        # Incrementally update mean and size
        cluster['mean'] = (cluster['mean'] * cluster['size'] + pixel_value) / (cluster['size'] + 1)
        cluster['pixels'].append(coord)
        cluster['size'] += 1

    # Process first row
    for j in range(1, w):
        pixel_value = img[0, j]
        added = False
        for cluster in clusters:
            if abs(pixel_value - cluster['mean']) <= threshold:
                add_pixel_to_cluster(cluster, pixel_value, (0, j))
                clustered_img[0, j] = clusters.index(cluster) + 1
                added = True
                break
        if not added:
            cluster_id += 1
            clusters.append({'mean': pixel_value, 'pixels': [(0, j)], 'size': 1})
            clustered_img[0, j] = cluster_id

    # Process remaining rows
    for i in range(1, h):
        for j in range(w):
            pixel_value = img[i, j]
            added = False
            for cluster in clusters:
                if abs(pixel_value - cluster['mean']) <= threshold:
                    add_pixel_to_cluster(cluster, pixel_value, (i, j))
                    clustered_img[i, j] = clusters.index(cluster) + 1
                    added = True
                    break
            if not added:
                cluster_id += 1
                clusters.append({'mean': pixel_value, 'pixels': [(i, j)], 'size': 1})
                clustered_img[i, j] = cluster_id

    # Merge small clusters safely without modifying lists during iteration
    small_clusters = [c for c in clusters if c['size'] < min_cluster_size]

    for cluster in small_clusters:
        for x, y in cluster['pixels']:
            # Find closest cluster excluding itself
            other_clusters = [c for c in clusters if c is not cluster]
            closest = min(other_clusters, key=lambda c: abs(img[x, y] - c['mean']))
            clustered_img[x, y] = clusters.index(closest) + 1
            add_pixel_to_cluster(closest, img[x, y], (x, y))

        # Mark small cluster as empty
        cluster['pixels'] = []
        cluster['size'] = 0
        cluster['mean'] = 0

    return clustered_img



def apply_vertical_segmentation(img, threshold=45, min_segment_height=5):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    h, w = img.shape
    result = np.zeros_like(img, dtype=np.uint8)
    cluster_id = 1
    
    for j in range(w):  # For each column
        current_val = img[0, j]
        segment_start = 0
        
        for i in range(1, h):  # For each pixel in column
            if abs(int(img[i, j]) - int(current_val)) > threshold:
                # Only create a new segment if the previous one was large enough
                if (i - segment_start) >= min_segment_height:
                    result[segment_start:i, j] = cluster_id
                    cluster_id = min(cluster_id + 25, 255)  # Limit to 255
                    segment_start = i
                    current_val = img[i, j]
        
        # Fill the remaining part of the column
        if (h - segment_start) >= min_segment_height:
            result[segment_start:h, j] = cluster_id
    
    # Normalize the output for better visualization
    if cluster_id > 1:  # If any segmentation occurred
        result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)
    
    return result