#!/usr/bin/env python3
"""Build route + elevation data for the Lake District walk website."""
import json, math, time, urllib.request, urllib.parse

# --- Each leg: ordered list of (lat, lon) anchor points following valleys/passes ---
LEGS = {
    "day4": {  # Windermere -> Grasmere (Thirlmere Way / via Rydal)
        "anchors": [
            (54.4136, -2.9080),  # Windermere station
            (54.4286, -2.9300),  # towards Ambleside (Troutbeck side / Wansfell foot)
            (54.4337, -2.9620),  # Ambleside
            (54.4470, -2.9870),  # Rydal
            (54.4490, -3.0080),  # Rydal Water north
            (54.4560, -3.0180),  # Grasmere village
            (54.4609, -3.0250),  # Grasmere YHA (Butharlyp How)
        ],
    },
    "day5": {  # Grasmere -> Borrowdale (Rosthwaite) via Far Easedale & Greenup Edge
        "anchors": [
            (54.4609, -3.0250),  # Grasmere YHA
            (54.4660, -3.0420),  # Far Easedale foot
            (54.4770, -3.0750),  # Far Easedale head
            (54.4880, -3.0980),  # Greenup Edge approach
            (54.4980, -3.1090),  # Greenup Edge (pass ~600m)
            (54.5120, -3.1280),  # Greenup Gill descent
            (54.5200, -3.1410),  # Stonethwaite
            (54.5253, -3.1450),  # Rosthwaite
            (54.5208, -3.1556),  # Borrowdale YHA (Longthwaite)
        ],
    },
    "day6": {  # Borrowdale -> Black Sail via Honister & Loft Beck
        "anchors": [
            (54.5208, -3.1556),  # Borrowdale YHA
            (54.5130, -3.1700),  # Seatoller
            (54.5085, -3.1930),  # Honister Pass (slate mine)
            (54.5085, -3.2050),  # Grey Knotts / Brandreth flank
            (54.5060, -3.2230),  # Loft Beck top
            (54.4990, -3.2330),  # Loft Beck foot
            (54.5003, -3.2448),  # Black Sail YHA (OSM)
        ],
    },
    "day7": {  # Optional: Haystacks from Black Sail via Scarth Gap (out and back)
        "anchors": [
            (54.5003, -3.2448),  # Black Sail YHA (OSM)
            (54.5040, -3.2520),  # Scarth Gap approach
            (54.5081, -3.2535),  # Scarth Gap pass
            (54.5072, -3.2473),  # Haystacks summit (OSM)
            (54.5054, -3.2412),  # Innominate Tarn
            (54.5072, -3.2473),  # back over summit
            (54.5081, -3.2535),  # Scarth Gap
            (54.5040, -3.2520),  # descent
            (54.5003, -3.2448),  # Black Sail YHA
        ],
    },
    "day8": {  # Black Sail -> Ennerdale YHA (valley walk)
        "anchors": [
            (54.5003, -3.2448),  # Black Sail YHA (OSM)
            (54.5040, -3.2700),  # Ennerdale forest road
            (54.5080, -3.3000),  # along River Liza
            (54.5149, -3.3260),  # Ennerdale YHA, Gillerthwaite (OSM)
        ],
    },
    "day8alt": {  # Alternative: Black Sail -> Buttermere (drop-off) -> Red Pike col -> Ennerdale YHA
        "anchors": [
            (54.5003, -3.2448),  # Black Sail YHA
            (54.5040, -3.2520),  # climb
            (54.5081, -3.2535),  # Scarth Gap pass
            (54.5150, -3.2560),  # descend Scarth Beck
            (54.5200, -3.2580),  # Peggy's Bridge
            (54.5249, -3.2500),  # Gatesgarth
            (54.5300, -3.2600),  # Buttermere SW shore
            (54.5360, -3.2700),  # lakeshore path
            (54.5410, -3.2760),  # Buttermere village (drop-off)
            (54.5400, -3.2900),  # Scale Bridge / moor path
            (54.5418, -3.3146),  # Scale Force (OSM)
            (54.5330, -3.3180),  # up Scale Beck
            (54.5290, -3.3200),  # col between Red Pike & Starling Dodd
            (54.5220, -3.3230),  # descend to Ennerdale forest
            (54.5149, -3.3260),  # Ennerdale YHA (OSM)
        ],
    },
    "day9": {  # Ennerdale YHA -> Whitehaven (Corkickle) reverse C2C
        "anchors": [
            (54.5149, -3.3260),  # Ennerdale YHA (OSM)
            (54.5190, -3.3650),  # Ennerdale Water south shore
            (54.5210, -3.3950),  # Anglers' Crag
            (54.5230, -3.4180),  # west end of lake
            (54.5292, -3.4391),  # Ennerdale Bridge (OSM)
            (54.5180, -3.4700),  # Nannycatch
            (54.5090, -3.5000),  # Dent flank
            (54.5070, -3.5226),  # Cleator (OSM)
            (54.5145, -3.5377),  # Moor Row (OSM)
            (54.5417, -3.5822),  # Corkickle station (OSM)
            (54.5490, -3.5860),  # Whitehaven harbour
        ],
    },
}

import os, sys
REBUILD = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else set(LEGS)
EXISTING = {}
if os.path.exists("route_data.json"):
    with open("route_data.json") as f:
        EXISTING = json.load(f)
LEGS = {k: v for k, v in LEGS.items() if k in REBUILD}

def haversine(a, b):
    R = 6371000.0
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def densify(anchors, step_m=70):
    pts = []
    for i in range(len(anchors) - 1):
        a, b = anchors[i], anchors[i+1]
        d = haversine(a, b)
        n = max(1, int(d // step_m))
        for k in range(n):
            t = k / n
            pts.append((a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t))
    pts.append(anchors[-1])
    return pts

def fetch_elev(points):
    elevs = []
    B = 100
    for i in range(0, len(points), B):
        chunk = points[i:i+B]
        lats = ",".join(f"{p[0]:.5f}" for p in chunk)
        lons = ",".join(f"{p[1]:.5f}" for p in chunk)
        url = "https://api.open-meteo.com/v1/elevation?" + urllib.parse.urlencode(
            {"latitude": lats, "longitude": lons})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    data = json.load(r)
                elevs.extend(data["elevation"])
                break
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(2)
        time.sleep(0.3)
    return elevs

out = dict(EXISTING)
for day, leg in LEGS.items():
    pts = densify(leg["anchors"])
    elevs = fetch_elev(pts)
    # light smoothing that preserves peaks (center-weighted)
    sm = elevs[:]
    for i in range(1, len(elevs)-1):
        sm[i] = (elevs[i-1] + 2*elevs[i] + elevs[i+1]) / 4.0
    # cumulative distance + ascent/descent
    cum = 0.0
    dist_km, ascent, descent = [], 0.0, 0.0
    prof = []
    for i, p in enumerate(pts):
        if i > 0:
            cum += haversine(pts[i-1], p)
            dz = sm[i] - sm[i-1]
            if dz > 0: ascent += dz
            else: descent += -dz
        dist_km.append(round(cum/1000.0, 3))
        prof.append([round(cum/1000.0, 3), round(sm[i], 1)])
    out[day] = {
        "coords": [[round(p[0], 5), round(p[1], 5)] for p in pts],
        "profile": prof,
        "distance_km": round(cum/1000.0, 1),
        "ascent_m": round(ascent),
        "descent_m": round(descent),
        "min_elev": round(min(sm)),
        "max_elev": round(max(sm)),
    }
    print(f"{day}: {out[day]['distance_km']} km, +{out[day]['ascent_m']} m / -{out[day]['descent_m']} m, "
          f"max {out[day]['max_elev']} m, pts={len(pts)}")

with open("route_data.json", "w") as f:
    json.dump(out, f)
print("WROTE route_data.json")
