from PIL import Image
import os

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
    with Image.open(os.path.join(image_dir, image_file)) as img:
        width, height = img.size
        max_width = max(max_width, width)
        max_height = max(max_height, height)

# Process the images
for image_file in image_files:
    with Image.open(os.path.join(image_dir, image_file)) as img:
        width, height = img.size

        # Scale the image to fill the max dimensions while maintaining aspect ratio
        if width > height:
            new_width = max_width
            new_height = int(max_width * height / width)
        else:
            new_height = max_height
            new_width = int(max_height * width / height)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Create a new image with transparent background
        new_img = Image.new("RGBA", (max_width, max_height))

        # Paste the resized image onto the transparent background
        box = (int((max_width - new_width) / 2), int((max_height - new_height) / 2))
        new_img.paste(img, box)

        # Save the image
        # new_img.save(os.path.join(image_dir, "resized_" + image_file))
        new_img.save(os.path.join(image_dir, "resized_" + os.path.splitext(image_file)[0] + ".png")) # if you want to keep transparency
