import os
import json
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

START_URL = "https://viva-futbol.x.yupoo.com/albums/167911975?uid=1"

DOWNLOAD_FOLDER = "folder1"
MAX_RETRIES = 3
THREADS = 5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# -------------------------------------------------------
def fetch_page(url):
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception:
            pass
        time.sleep(2)
    return None

# -------------------------------------------------------
def scrape_all_pages():
    page = 1
    albums = []
    seen = set()

    while True:
        print(f"Checking page {page}...")

        url = f"{START_URL}?ajax=1&page={page}"
        html = fetch_page(url)
        if not html:
            break

        soup = BeautifulSoup(html, "html.parser")
        page_albums = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/albums/" in href:
                full = "https://viva-futbol.x.yupoo.com" + href
                title = a.get("title") or a.get_text(strip=True) or "Unknown"
                if full not in seen:
                    seen.add(full)
                    page_albums.append({"title": title, "url": full})

        if not page_albums:
            print("No more albums. Stopping pagination.")
            break

        albums.extend(page_albums)
        page += 1

    print(f"✔ Total albums: {len(albums)}")
    return albums

# -------------------------------------------------------
def scrape_album_images(album_url):
    html = fetch_page(album_url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    images = set()

    for img in soup.find_all("img"):
        src = img.get("data-origin-src") or img.get("data-src") or img.get("src")
        if src and "photo.yupoo.com" in src:
            if src.startswith("//"):
                src = "https:" + src
            images.add(src)

    return list(images)

# -------------------------------------------------------
def download_image(url, folder, index, referer):
    ext = url.split(".")[-1].split("?")[0]
    filename = f"{index}.{ext}"
    filepath = os.path.join(folder, filename)

    headers = dict(HEADERS)
    headers["Referer"] = referer

    for _ in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(r.content)
                return
        except Exception:
            pass
        time.sleep(1)

# -------------------------------------------------------
def download_images(album_title, image_urls, album_url):
    safe = "".join([c if c.isalnum() or c in " _-" else "_" for c in album_title])[:100]
    path = os.path.join(DOWNLOAD_FOLDER, safe)
    os.makedirs(path, exist_ok=True)

    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for i, url in enumerate(image_urls, 1):
            ex.submit(download_image, url, path, i, album_url)

# -------------------------------------------------------
def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    print("📌 Scraping albums with AJAX pagination...")
    albums = scrape_all_pages()

    all_data = []

    for alb in albums:
        print(f"\n📂 Album: {alb['title']}")
        imgs = scrape_album_images(alb["url"])
        print(f" → {len(imgs)} images.")
        if imgs:
            download_images(alb["title"], imgs, alb["url"])
        all_data.append({"title": alb["title"], "url": alb["url"], "images": imgs})

    with open("yupoo_products.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print("\n🎉 DONE.")

if __name__ == "__main__":
    main()
