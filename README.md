# Coast to Coast · Lake District Walk — July 2026

A single-page website for our walking holiday: Windermere → Grasmere → Borrowdale → Black Sail → Ennerdale → Whitehaven, 3–9 July 2026. Interactive maps (Leaflet + OpenTopoMap) and elevation profiles for every day.

## Publish on GitHub Pages

1. Create a new repository on GitHub (e.g. `lake-district-walk`), public.
2. Upload `index.html` (and this `README.md`) to the repository root — drag-and-drop on github.com works fine.
3. In the repo: **Settings → Pages → Branch: `main` / folder: `/ (root)` → Save**.
4. After a minute the site is live at `https://<your-username>.github.io/lake-district-walk/`.
5. Send that link to your friends.

## Notes

- Everything is in one file (`index.html`) — no build step, no API keys.
- Routes follow real OSM hiking paths, routed with BRouter (hiking-mountain profile); distances, elevation profiles and ascent totals come from the routed tracks. Still indicative — carry OS maps for navigation.
- `build_routes.py` and `gen_site.py` regenerate the data and page if you want to tweak routes: edit the via points/text, then run `python3 build_routes.py && python3 gen_site.py`.
