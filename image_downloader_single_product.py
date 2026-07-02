import os
import re
import time
import requests
from requests.exceptions import ChunkedEncodingError, RequestException

# =========================
# CONFIGURATION
# =========================

ALBUM_URL = "https://viva-futbol.x.yupoo.com/albums/168283374?uid=1"
SAVE_DIR = "images_HD/Italy24_blue_windbreaker_jacket_S-XXL11"
MAX_RETRY = 3
TIMEOUT = 25

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# SESSION
# =========================

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": ALBUM_URL,
    "Accept": "image/webp,image/*,*/*;q=0.8",
})

# =========================
# RÉCUPÉRER LA PAGE
# =========================

print("📥 Chargement de l'album...")
response = session.get(ALBUM_URL, timeout=TIMEOUT)
response.raise_for_status()
html = response.text

# =========================
# EXTRAIRE LES IMAGES HD
# =========================

# data-origin-src = vraie image (pas miniature)
raw_urls = set(re.findall(
    r'data-origin-src="(//photo\.yupoo\.com/[^"]+)"',
    html
))

print(f"🖼️ {len(raw_urls)} images trouvées")

# =========================
# TÉLÉCHARGEMENT
# =========================

for index, url in enumerate(raw_urls, start=1):
    # URL complète + forcer HD
    url = "https:" + url
    url = url.replace("small", "big").replace("medium", "big")

    filename = os.path.join(SAVE_DIR, url.split("/")[-1])
    print(f"[{index}/{len(raw_urls)}] Téléchargement...")

    for attempt in range(1, MAX_RETRY + 1):
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()

            with open(filename, "wb") as f:
                f.write(r.content)

            print("   ✅ OK")
            break

        except ChunkedEncodingError:
            print("   ⚠️ Connexion coupée, retry...")
            time.sleep(2)

        except RequestException as e:
            print("   ❌ Erreur :", e)
            break

print("\n🎉 Téléchargement terminé avec succès")
