#!/usr/bin/env python3
"""Build route + elevation data for the Lake District walk website.

Routes follow real hiking paths via BRouter (OSM, hiking-mountain profile);
distance, geometry and elevation come from the routed track.
Usage: python3 build_routes.py [day4,day7,...]   (default: all legs)
"""
import json, math, os, sys, time, urllib.request, urllib.parse

# Via points guiding each leg along the planned route (lat, lon)
LEGS = {
    "day4": [  # Windermere YHA -> Grasmere
        (54.4039, -2.9175),  # YHA Windermere, Bridge Lane (OSM)
        (54.4337, -2.9620),  # Ambleside
        (54.4470, -2.9870),  # Rydal
        (54.4609, -3.0250),  # Grasmere YHA (Butharlyp How)
    ],
    "day5": [  # Grasmere -> Borrowdale via Far Easedale & Greenup Edge
        (54.4609, -3.0250),  # Grasmere YHA
        (54.4770, -3.0750),  # Far Easedale head
        (54.4980, -3.1090),  # Greenup Edge
        (54.5200, -3.1410),  # Stonethwaite
        (54.5208, -3.1556),  # Borrowdale YHA (Longthwaite)
    ],
    "day6": [  # Borrowdale -> Black Sail via Honister & Loft Beck
        (54.5208, -3.1556),  # Borrowdale YHA
        (54.5085, -3.1930),  # Honister Pass
        (54.5060, -3.2230),  # Loft Beck top
        (54.5003, -3.2448),  # Black Sail YHA (OSM)
    ],
    "day7": [  # Optional: Haystacks loop via Scarth Gap & Innominate Tarn
        (54.5003, -3.2448),  # Black Sail YHA
        (54.5081, -3.2535),  # Scarth Gap pass
        (54.5072, -3.2473),  # Haystacks summit (OSM)
        (54.5054, -3.2412),  # Innominate Tarn
        (54.5003, -3.2448),  # Black Sail YHA
    ],
    "day8": [  # Black Sail -> Ennerdale YHA (valley)
        (54.5003, -3.2448),  # Black Sail YHA
        (54.5080, -3.3000),  # River Liza forest road
        (54.5149, -3.3260),  # Ennerdale YHA, Gillerthwaite (OSM)
    ],
    "day8alt": [  # Black Sail -> Gatesgarth (drop-off) -> Bleaberry Tarn -> Ennerdale YHA
        (54.5003, -3.2448),  # Black Sail YHA
        (54.5081, -3.2535),  # Scarth Gap pass
        (54.5218, -3.2563),  # Gatesgarth (Martina's drop-off)
        (54.5390, -3.2790),  # Buttermere lake foot
        (54.5302, -3.2870),  # Sourmilk Gill climb
        (54.5273, -3.2903),  # Bleaberry Tarn (OSM)
        (54.5149, -3.3260),  # Ennerdale YHA (OSM)
    ],
    "day9": [  # Ennerdale YHA -> Whitehaven (reverse C2C)
        (54.5149, -3.3260),  # Ennerdale YHA
        (54.5230, -3.4180),  # west end of Ennerdale Water
        (54.5292, -3.4391),  # Ennerdale Bridge (OSM)
        (54.5180, -3.4700),  # Nannycatch
        (54.5070, -3.5226),  # Cleator (OSM)
        (54.5151, -3.5513),  # Scalegill Hall bus stop, Bigrigg (bus to Corkickle)
    ],
}

def haversine(a, b):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def brouter(viapoints):
    lonlats = "|".join(f"{lon:.5f},{lat:.5f}" for lat, lon in viapoints)
    url = ("https://brouter.de/brouter?lonlats=" + urllib.parse.quote(lonlats, safe=",|")
           + "&profile=hiking-mountain&alternativeidx=0&format=geojson")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
            feat = d["features"][0]
            props = feat["properties"]
            coords = feat["geometry"]["coordinates"]  # [lon, lat, ele]
            return coords, int(props["track-length"]), int(props["filtered ascend"])
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3)

REBUILD = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else set(LEGS)
out = {}
if os.path.exists("route_data.json"):
    with open("route_data.json") as f:
        out = json.load(f)

for day in [k for k in LEGS if k in REBUILD]:
    coords, dist_m, ascend = brouter(LEGS[day])
    pts = [(c[1], c[0]) for c in coords]
    elev = [c[2] if len(c) > 2 and c[2] is not None else None for c in coords]
    # fill any missing elevations by neighbour interpolation
    for i, e in enumerate(elev):
        if e is None:
            prev = next((elev[j] for j in range(i-1, -1, -1) if elev[j] is not None), 0)
            elev[i] = prev
    # light centre-weighted smoothing for the profile/descent
    sm = elev[:]
    for i in range(1, len(elev)-1):
        sm[i] = (elev[i-1] + 2*elev[i] + elev[i+1]) / 4.0
    cum, prof, descent = 0.0, [], 0.0
    for i, p in enumerate(pts):
        if i > 0:
            cum += haversine(pts[i-1], p)
            dz = sm[i] - sm[i-1]
            if dz < 0:
                descent += -dz
        prof.append([round(cum/1000.0, 3), round(sm[i], 1)])
    # scale profile x to BRouter's true track length (haversine slightly underreads)
    scale = (dist_m/1000.0) / (cum/1000.0) if cum else 1.0
    prof = [[round(x*scale, 3), y] for x, y in prof]
    out[day] = {
        "coords": [[round(la, 5), round(lo, 5)] for la, lo in pts],
        "profile": prof,
        "distance_km": round(dist_m/1000.0, 1),
        "ascent_m": ascend,
        "descent_m": round(descent),
        "min_elev": round(min(sm)),
        "max_elev": round(max(sm)),
    }
    print(f"{day}: {out[day]['distance_km']} km, +{ascend} m / -{out[day]['descent_m']} m, "
          f"max {out[day]['max_elev']} m, pts={len(pts)}")
    time.sleep(1)

with open("route_data.json", "w") as f:
    json.dump(out, f)
print("WROTE route_data.json")
