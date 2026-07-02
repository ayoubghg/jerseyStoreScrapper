import os

base_folder = "images_HD/Spain_24_blue_Windbreaker_Jacket_size_S-2XL9"

# accepted image extensions
image_ext = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}

for folder in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder)

    if not os.path.isdir(folder_path):
        continue

    # convert folder name for naming only (do NOT rename folder)
    clean_folder_name = folder.replace(" ", "_")

    # get images
    images = [
        f for f in os.listdir(folder_path)
        if os.path.splitext(f.lower())[1] in image_ext
    ]

    images.sort()

    # rename images
    for idx, img in enumerate(images, start=1):
        old_path = os.path.join(folder_path, img)
        ext = os.path.splitext(img)[1].lower()
        new_name = f"{clean_folder_name}_{idx}{ext}"
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        print(f"{old_path} → {new_path}")

print("\n✔ DONE! Only images renamed. Folder names unchanged.")
