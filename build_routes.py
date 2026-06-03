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
            (54.5070, -3.2050),  # Grey Knotts / Brandreth flank
            (54.5060, -3.2230),  # Loft Beck top
            (54.5070, -3.2380),  # Loft Beck descent
            (54.5060, -3.2480),  # Black Sail YHA
        ],
    },
    "day7": {  # Optional: Haystacks from Black Sail via Scarth Gap (out and back)
        "anchors": [
            (54.5060, -3.2480),  # Black Sail YHA
            (54.5018, -3.2400),  # Scarth Gap approach
            (54.5000, -3.2330),  # Scarth Gap pass
            (54.5044, -3.2247),  # Haystacks summit
            (54.5030, -3.2200),  # Innominate Tarn
            (54.5044, -3.2247),  # back over summit
            (54.5000, -3.2330),  # Scarth Gap
            (54.5060, -3.2480),  # Black Sail YHA
        ],
    },
    "day8": {  # Black Sail -> Ennerdale YHA (valley walk)
        "anchors": [
            (54.5060, -3.2480),  # Black Sail YHA
            (54.5130, -3.2720),  # Ennerdale forest road
            (54.5200, -3.3050),  # along River Liza
            (54.5240, -3.3300),  # Gillerthwaite
            (54.5290, -3.3460),  # Ennerdale YHA (Cat Crag / Gillerthwaite)
        ],
    },
    "day9": {  # Ennerdale YHA -> Whitehaven (Corkickle) reverse C2C
        "anchors": [
            (54.5290, -3.3460),  # Ennerdale YHA
            (54.5360, -3.3760),  # Ennerdale Water head
            (54.5410, -3.4050),  # along Ennerdale Water
            (54.5350, -3.4280),  # Ennerdale Bridge
            (54.5290, -3.4600),  # Kinniside / Nannycatch
            (54.5230, -3.4980),  # Cleator Moor approach
            (54.5210, -3.5180),  # Cleator
            (54.5300, -3.5400),  # Dent flank
            (54.5380, -3.5600),  # Moor Row
            (54.5440, -3.5810),  # Corkickle station
            (54.5490, -3.5860),  # Whitehaven harbour
        ],
    },
}

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

out = {}
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
