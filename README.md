# Tamil OTT Auto (1080p)

This repo automates Tamil OTT movie downloads:

- **Scraper**: Pulls latest 1TamilMV posts (20 items), extracts magnets, saves to `tamilmv_feed.xml` (max 100 items).
- **Prowlarr**: Use GitHub Pages URL of `tamilmv_feed.xml` as Torznab indexer.
- **JustWatch Tamil**: Scrapes latest Tamil OTT movies, adds them into Radarr.
- **Radarr**: Movies are added with quality profile ID=2 (1080p).

## Setup

1. Fork repo, enable GitHub Pages (serve from root).
2. Add repo secrets:
   - `TAMILMV_REDIRECTOR` (Cloudflare Pages redirect to 1TamilMV mirror)
   - `RADARR_URL`, `RADARR_API_KEY`, `RADARR_ROOT`, `RADARR_QUALITY_PROFILE_ID`
3. Enable Actions → Tamil OTT Auto.
