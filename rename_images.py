import os


FOLDER_PATH = "./images_HD/Italy24_blue_windbreaker_jacket_S-XXL11"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

folder_name = os.path.basename(os.path.normpath(FOLDER_PATH))

files = [
    f for f in os.listdir(FOLDER_PATH)
    if f.lower().endswith(IMAGE_EXTENSIONS)
]

files.sort()  


for index, filename in enumerate(files, start=1):
    old_path = os.path.join(FOLDER_PATH, filename)
    extension = os.path.splitext(filename)[1]
    new_name = f"{folder_name}_{index}{extension}"
    new_path = os.path.join(FOLDER_PATH, new_name)

    os.rename(old_path, new_path)

print("✅ Renommage terminé")
