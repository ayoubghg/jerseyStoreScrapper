import os

# dossier principal
base_folder = "wind_north"

# extensions d'images acceptées
image_ext = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff"}

missing_folders_file = "missing_images.txt"

with open(missing_folders_file, "w", encoding="utf-8") as out:
    # parcourir tous les sous-dossiers
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)

        # ignorer les fichiers simples
        if not os.path.isdir(folder_path):
            continue

        # vérifier s'il contient une image
        has_image = False
        for file in os.listdir(folder_path):
            _, ext = os.path.splitext(file.lower())
            if ext in image_ext:
                has_image = True
                break
        
        # si aucune image trouvée → enregistrer le nom
        if not has_image:
            out.write(folder + "\n")
            print(f"[!] Aucune image dans : {folder}")

print("\nTerminé ! Vérifiez missing_images.txt")
