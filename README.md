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
- Day distances follow the planned routes (plotaroute / AllTrails / OS Maps links on each day).
- Map lines, elevation profiles and ascent totals are approximations sampled from open terrain data (Copernicus DEM via open-meteo) — use proper OS maps for navigation.
- `build_routes.py` and `gen_site.py` regenerate the data and page if you want to tweak routes: edit the waypoints/text, then run `python3 build_routes.py && python3 gen_site.py`.
