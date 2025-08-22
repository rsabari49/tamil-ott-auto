#!/usr/bin/env python3
import requests, os, sys, traceback

RADARR_URL = os.getenv("RADARR_URL")
API_KEY = os.getenv("RADARR_API_KEY")
QUALITY_PROFILE_ID = int(os.getenv("RADARR_QUALITY_PROFILE_ID", "2"))  # default 1080p
LANGUAGE_PROFILE_ID = int(os.getenv("RADARR_LANGUAGE_PROFILE_ID", "1"))

HEADERS = {"X-Api-Key": API_KEY}

def get_root_folder():
    """Fetch the first root folder configured in Radarr"""
    url = f"{RADARR_URL}/api/v3/rootFolder"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    folders = r.json()
    if not folders:
        raise RuntimeError("❌ No root folders found in Radarr. Please configure one in Radarr UI.")
    print(f"📂 Using Radarr root folder: {folders[0]['path']}")
    return folders[0]["path"]  # first available root folder

def fetch_justwatch():
    """Fetch latest Tamil movies from JustWatch (first page, 20 items)"""
    url = "https://apis.justwatch.com/content/titles/en_IN/popular"
    payload = {
        "page_size": 20,
        "page": 1,
        "content_types": ["movie"]
    }
    print("🌐 Fetching JustWatch movies...")
    r = requests.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    results = []
    for item in data.get("items", []):
        title = item.get("title")
        year = item.get("original_release_year")
        if not title:
            continue
        # crude Tamil filter
        if "ta" not in str(item.get("scoring", "")) and "Tamil" not in str(item.get("original_language", "")):
            continue
        results.append({"title": title, "year": year})
    print(f"🎬 Found {len(results)} Tamil movies on JustWatch")
    return results

def add_to_radarr(movie, root_folder):
    """Send movie request to Radarr"""
    payload = {
        "title": movie["title"],
        "year": movie["year"],
        "qualityProfileId": QUALITY_PROFILE_ID,
        "rootFolderPath": root_folder,
        "monitored": True,
        "addOptions": {"searchForMovie": True},
        "languageProfileId": LANGUAGE_PROFILE_ID
    }
    url = f"{RADARR_URL}/api/v3/movie"
    r = requests.post(url, json=payload, headers=HEADERS)
    if r.status_code in (200, 201):
        print(f"✅ Added: {movie['title']} ({movie['year']})")
    else:
        print(f"❌ Failed to add {movie['title']} ({movie['year']}): {r.status_code}")
        print("Response:", r.text)

def main():
    try:
        root_folder = get_root_folder()
        movies = fetch_justwatch()
        if not movies:
            print("⚠️ No Tamil movies found on JustWatch")
        for m in movies:
            add_to_radarr(m, root_folder)
    except Exception as e:
        print("🚨 Script crashed with error:", str(e))
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
