#!/usr/bin/env python3
import requests, os, datetime

RADARR_URL = os.getenv("RADARR_URL")
API_KEY = os.getenv("RADARR_API_KEY")
ROOT = os.getenv("RADARR_ROOT", "/movies")
QUALITY_PROFILE_ID = int(os.getenv("RADARR_QUALITY_PROFILE_ID", "2"))  # default 1080p
LANGUAGE_PROFILE_ID = int(os.getenv("RADARR_LANGUAGE_PROFILE_ID", "1"))

def fetch_justwatch():
    url = "https://apis.justwatch.com/content/titles/en_IN/popular"
    params = {"body": {"page_size": 20, "page": 1, "content_types": ["movie"]}}
    r = requests.post(url, json=params)
    r.raise_for_status()
    data = r.json()
    results = []
    for item in data.get("items", []):
        title = item.get("title")
        original_release_year = item.get("original_release_year")
        if not title: continue
        # crude Tamil filter
        if "ta" not in str(item.get("scoring", "")) and "Tamil" not in str(item.get("original_language", "")):
            continue
        results.append({"title": title, "year": original_release_year})
    return results

def add_to_radarr(movie):
    payload = {
        "title": movie["title"],
        "year": movie["year"],
        "qualityProfileId": QUALITY_PROFILE_ID,
        "rootFolderPath": ROOT,
        "monitored": True,
        "addOptions": {"searchForMovie": True},
        "languageProfileId": LANGUAGE_PROFILE_ID
    }
    url = f"{RADARR_URL}/api/v3/movie"
    headers = {"X-Api-Key": API_KEY}
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code in (200, 201):
        print("Added:", movie)
    else:
        print("Failed:", r.text)

def main():
    movies = fetch_justwatch()
    for m in movies:
        add_to_radarr(m)

if __name__ == "__main__":
    main()
