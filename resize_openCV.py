import os
import cv2
import numpy as np

# Directory containing images
image_dir = "."

# Get a list of all the image files in the directory
image_files = [f for f in os.listdir(image_dir) if (f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')) and not f.startswith('resized_')]
# image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]

# Initialize maximum width and height
max_width = 5
max_height = 5

# Determine the maximum dimensions
for image_file in image_files:
    img = cv2.imread(os.path.join(image_dir, image_file))
    height, width = img.shape[:2]
    max_width = max(max_width, width)
    max_height = max(max_height, height)

# Process the images
for image_file in image_files:
    img = cv2.imread(os.path.join(image_dir, image_file), cv2.IMREAD_UNCHANGED)

    # OpenCV does not handle transparency in the same way as Pillow,
    # So we need to check if the image has an alpha channel, if not, add one.
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    height, width = img.shape[:2]
    # Compute the scaling factor
    if width > height:
        new_width = max_width
        new_height = int(height * max_width / width)
    else:
        new_height = max_height
        new_width = int(width * max_height / height)
    
    img = cv2.resize(img, (new_width, new_height))

    # Create a new image with transparent background
    new_img = np.zeros((max_height, max_width, 4), np.uint8)
    # If you want to create a semi-transparent background, you can adjust the alpha value. For example, an alpha value of 255 in the new image will create a fully opaque black background
    # new_img[:,:,3] = 255

    # Compute the top left corner of the region to paste the image
    top_left = ((max_width - new_width) // 2, (max_height - new_height) // 2)

    # Paste the resized image onto the transparent background
    new_img[top_left[1]:top_left[1]+new_height, top_left[0]:top_left[0]+new_width] = img

    # Save the image
    cv2.imwrite(os.path.join(image_dir, "resized_" + os.path.splitext(image_file)[0] + ".png"), new_img)