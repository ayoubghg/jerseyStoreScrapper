from PIL import Image
import os

# Adjust minimum quality resolution here:
MIN_WIDTH = 300
MIN_HEIGHT = 300

def remove_small_images(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                path = os.path.join(root, file)

                try:
                    with Image.open(path) as img:
                        w, h = img.size

                        # Delete if image is too small
                        if w < MIN_WIDTH or h < MIN_HEIGHT:
                            print(f"Deleting {path} ({w}x{h})")
                            os.remove(path)

                except Exception as e:
                    # Delete corrupted images too
                    print(f"Deleting corrupted file: {path}")
                    os.remove(path)

# Run it on your folder
folder=input("Folder's name : ")
remove_small_images(folder)
