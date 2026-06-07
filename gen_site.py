#!/usr/bin/env python3
"""Generate index.html for the Lake District walk site, embedding route data."""
import json

with open("route_data.json") as f:
    R = json.load(f)

# Per-day editorial metadata. distance_km uses Greg's figures from his linked routes.
DAYS = [
    {
        "key": "day3", "n": 0, "date": "Fri 3 July", "kind": "travel",
        "title": "Arrive in Windermere",
        "from_to": "Travel day",
        "train": "Train arrives 19:40",
        "distance_km": None, "stay": "Windermere YHA  ·  booked",
        "stay_url": "https://www.yha.org.uk/hostel/yha-windermere",
        "desc": "Arrive by train at <strong>19:40</strong> into Windermere. Evening to settle in, "
                "grab dinner and an early night before the walking begins. Windermere is the gateway "
                "to the central Lakes — the perfect launch point.",
        "links": [],
    },
    {
        "key": "day4", "n": 1, "date": "Sat 4 July", "kind": "walk",
        "title": "Windermere → Grasmere",
        "from_to": "Windermere YHA to Grasmere YHA",
        "distance_km": 16, "stay": "Grasmere YHA (Butharlyp How)  ·  booked",
        "stay_url": "https://www.yha.org.uk/hostel/yha-grasmere-butharlyp-howe",
        "desc": "A gentle warm-up day on rolling hills from the hostel via Ambleside and Rydal Water "
                "into Wordsworth’s Grasmere. Easy gradients, classic Lakeland views, and a famous "
                "gingerbread shop waiting at the end.",
        "links": [
            ("Route on plotaroute", "https://www.plotaroute.com/route/93466"),
            ("AllTrails: Thirlmere Way", "https://www.alltrails.com/en-gb/trail/england/cumbria/thirlmere-way-windermere-to-grasmere"),
        ],
    },
    {
        "key": "day5", "n": 2, "date": "Sun 5 July", "kind": "walk",
        "title": "Grasmere → Borrowdale",
        "from_to": "Grasmere YHA to Borrowdale YHA",
        "distance_km": 13, "stay": "Borrowdale YHA (Longthwaite)  ·  booked",
        "stay_url": "https://www.yha.org.uk/hostel/yha-borrowdale",
        "desc": "The first proper mountain day, on Wainwright’s Coast to Coast in reverse. Climb "
                "Far Easedale to the wild pass at <strong>Greenup Edge (~600 m)</strong>, then descend "
                "through Stonethwaite into the beautiful Borrowdale valley.",
        "links": [
            ("OS Maps: Rosthwaite to Grasmere", "https://explore.osmaps.com/route/19119818/alfred-wainwrights-coast-to-coast-walk-rosthwaite-to-grasmere"),
        ],
    },
    {
        "key": "day6", "n": 3, "date": "Mon 6 July", "kind": "walk",
        "title": "Borrowdale → Black Sail",
        "from_to": "Borrowdale YHA to Black Sail YHA",
        "distance_km": 9, "stay": "Black Sail YHA  ·  booked",
        "stay_url": "https://www.yha.org.uk/hostel/yha-black-sail",
        "desc": "Short but steep. Up through Seatoller and over Honister Pass, then a stiff climb to "
                "the <strong>~500 m</strong> top of Loft Beck before dropping into remote Ennerdale. "
                "Black Sail is England’s most isolated youth hostel — a former shepherd’s "
                "bothy ringed by mountains, with no road to it.",
        "links": [],
    },
    {
        "key": "day7", "n": 4, "date": "Tue 7 July", "kind": "optional",
        "title": "Black Sail · optional Haystacks",
        "from_to": "Rest day / optional summit",
        "distance_km": 6, "stay": "Black Sail YHA  ·  booked",
        "stay_url": "https://www.yha.org.uk/hostel/yha-black-sail",
        "desc": "A second night at Black Sail with an optional ascent of <strong>Haystacks (597 m)</strong> "
                "— Alfred Wainwright’s favourite fell, where his ashes were scattered beside "
                "Innominate Tarn. A short, rugged out-and-back over Scarth Gap rewards you with what "
                "many call the most beautiful summit in the Lakes. Bigger options straight from the "
                "hut: <strong>Great Gable (899 m)</strong>, <strong>Pillar (892 m)</strong>, or the "
                "<strong>Red Pike (826 m)</strong> &amp; <strong>Steeple (819 m)</strong> ridge.",
        "links": [],
    },
    {
        "key": "day8", "n": 5, "date": "Wed 8 July", "kind": "walk",
        "title": "Black Sail → Ennerdale",
        "from_to": "Black Sail YHA to Ennerdale YHA",
        "distance_km": 7, "stay": "Ennerdale YHA  ·  booked",
        "stay_url": "https://www.yha.org.uk/hostel/yha-ennerdale",
        "desc": "Two ways to Ennerdale today. <strong>Direct (solid line):</strong> an easy, mostly "
                "downhill valley walk following the River Liza through Ennerdale forest to the hostel "
                "at Gillerthwaite. <strong>Via Buttermere (dashed):</strong> back over Scarth Gap to "
                "Gatesgarth in the Buttermere valley to see Martina off, then along the lake through "
                "Burtness Wood and up beside Sourmilk Gill to Bleaberry Tarn, crossing the saddle by "
                "<strong>Red Pike (Buttermere, 755 m)</strong> before dropping to Ennerdale YHA.",
        "alt_key": "day8alt",
        "alt_label": "Via Buttermere",
        "alt_poi": [54.5218, -3.2563, "Gatesgarth — Martina’s drop-off"],
        "links": [],
    },
    {
        "key": "day9", "n": 6, "date": "Thu 9 July", "kind": "walk",
        "title": "Ennerdale → Whitehaven",
        "from_to": "Ennerdale YHA to Scalegill Hall, then bus to Corkickle",
        "distance_km": 17, "stay": "The Mansion Guesthouse, Whitehaven  ·  booked",
        "stay_url": "https://www.themansionguesthouse.co.uk/",
        "desc": "The final day, following the Coast to Coast in reverse past Ennerdale Bridge, through "
                "Nannycatch and Cleator to the <strong>Scalegill Hall bus stop</strong> at Bigrigg — "
                "then the <strong>bus to Corkickle / Whitehaven</strong> for a celebratory dinner and "
                "a night in town.",
        "links": [
            ("Coast to Coast: St Bees to Ennerdale Bridge", "https://www.paulbeal.com/coast-to-coast-walk/#h-coast-to-coast-walk-st-bees-to-ennerdale-bridge"),
        ],
    },
    {
        "key": "day10", "n": 7, "date": "Fri 10 July", "kind": "travel",
        "title": "Train home",
        "from_to": "Travel day",
        "train": "Train departs Corkickle 08:39",
        "distance_km": None, "stay": None,
        "stay_url": None,
        "desc": "Departure at <strong>08:39</strong> from Corkickle station (a 10–15 minute walk from "
                "Whitehaven harbour) to Lancaster. Farewell to the fells!",
        "links": [],
    },
]

# attach computed geo data; distances now come from BRouter's routed track
# along real OSM hiking paths, so use them as the headline figures
for d in DAYS:
    rd = R.get(d["key"])
    d["geo"] = rd  # may be None for travel day
    d["alt_geo"] = R.get(d["alt_key"]) if d.get("alt_key") else None
    if rd:
        d["distance_km"] = rd["distance_km"]

# high-contrast palette so routes stand out against OpenTopoMap's green terrain
COLORS = ["#9aa0a6", "#e8413c", "#ee7c2b", "#2f7fd1", "#8a4fc2", "#18a05c", "#d2308f", "#9aa0a6"]
for i, d in enumerate(DAYS):
    d["color"] = COLORS[i]

# totals
total_km = round(sum(d["distance_km"] for d in DAYS if d["distance_km"] and d["kind"] in ("walk",)))
total_ascent = sum(d["geo"]["ascent_m"] for d in DAYS if d["geo"] and d["kind"] == "walk")
walk_days = sum(1 for d in DAYS if d["kind"] == "walk")

PAYLOAD = {"days": DAYS, "totals": {"km": total_km, "ascent": total_ascent, "walk_days": walk_days}}

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Lake District Trek — July 2026</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
  integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root{
    --green:#2f8f4e; --green-d:#1f6b39; --rust:#c75c3a; --ink:#23302a;
    --stone:#6b7269; --paper:#f6f4ec; --card:#ffffff; --line:#e3e0d4;
    --shadow:0 6px 24px rgba(31,53,40,.10);
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    color:var(--ink);background:var(--paper);line-height:1.6}
  a{color:var(--green-d)}
  .wrap{max-width:1000px;margin:0 auto;padding:0 20px}

  header.hero{position:relative;color:#fff;text-align:center;padding:90px 20px 80px;
    background:linear-gradient(160deg,#1f6b39 0%,#2f8f4e 45%,#4a8c6a 100%);overflow:hidden}
  header.hero::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:70px;
    background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 70'><path d='M0 70 L0 40 L120 18 L240 46 L360 8 L480 40 L600 14 L720 44 L840 6 L960 38 L1080 16 L1200 42 L1200 70 Z' fill='%23f6f4ec'/></svg>") no-repeat center/cover}
  .hero .kicker{letter-spacing:.28em;text-transform:uppercase;font-size:.78rem;opacity:.9;margin-bottom:14px}
  .hero h1{margin:0;font-size:clamp(2.1rem,5vw,3.6rem);font-weight:800;line-height:1.08;text-shadow:0 2px 18px rgba(0,0,0,.18)}
  .hero p.sub{margin:16px auto 0;max-width:620px;font-size:1.05rem;opacity:.96}
  .hero .dates{margin-top:22px;display:inline-flex;gap:10px;flex-wrap:wrap;justify-content:center}
  .pill{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.32);
    padding:7px 14px;border-radius:999px;font-size:.9rem;backdrop-filter:blur(4px)}

  .stats{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin:-38px auto 10px;position:relative;z-index:3}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);
    padding:16px 22px;text-align:center;min-width:130px}
  .stat b{display:block;font-size:1.7rem;color:var(--green-d);line-height:1.1}
  .stat span{font-size:.8rem;color:var(--stone);text-transform:uppercase;letter-spacing:.06em}

  .section-title{text-align:center;margin:54px 0 6px;font-size:1.5rem}
  .section-sub{text-align:center;color:var(--stone);margin:0 0 26px}

  #overviewMap{height:420px;border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow);margin-bottom:10px}
  .legend{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin:14px 0 0;font-size:.86rem;color:var(--stone)}
  .legend i{display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:6px;vertical-align:-2px}

  .day{background:var(--card);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);
    margin:26px 0;overflow:hidden}
  .day-head{display:flex;align-items:center;gap:16px;padding:20px 24px;border-bottom:1px solid var(--line)}
  .daynum{flex:0 0 auto;width:58px;height:58px;border-radius:14px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;color:#fff;font-weight:800;line-height:1}
  .daynum small{font-size:.6rem;font-weight:600;opacity:.85;letter-spacing:.05em}
  .daynum b{font-size:1.5rem}
  .day-head .h{flex:1 1 auto;min-width:0}
  .day-head .date{font-size:.8rem;color:var(--stone);text-transform:uppercase;letter-spacing:.08em}
  .day-head h3{margin:2px 0 0;font-size:1.3rem}
  .day-head .route{color:var(--stone);font-size:.92rem}
  .badges{display:flex;gap:8px;flex-wrap:wrap}
  .badge{font-size:.82rem;background:#eef4ee;color:var(--green-d);border:1px solid #d4e6d8;
    padding:5px 11px;border-radius:999px;white-space:nowrap;font-weight:600}
  .badge.alt{background:#f6ece6;color:#a9482a;border-color:#ecd3c6}
  .badge.train{background:#e8eef7;color:#2b5797;border-color:#cdd9ec}
  .badge.grey{background:#eef0ee;color:#5c655c;border-color:#dfe2dd}
  .day-body{padding:20px 24px}
  .day-body p.desc{margin:0 0 16px}
  .stay{font-size:.92rem;margin:0 0 18px}
  .stay b{color:var(--ink)}
  .day-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:16px}
  @media(max-width:760px){.day-grid{grid-template-columns:1fr}}
  .map{height:300px;border-radius:14px;border:1px solid var(--line);overflow:hidden}
  .chartbox{height:300px;border-radius:14px;border:1px solid var(--line);background:#fbfbf7;padding:10px}
  .chartbox canvas{width:100%!important}
  .panel-label{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--stone);margin:0 0 6px}
  .links{margin-top:8px;font-size:.88rem}
  .links a{margin-right:14px;white-space:nowrap}
  .travel .day-body{color:var(--stone)}

  .logi{background:var(--card);border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);
    padding:26px 28px;margin:26px 0}
  .logi h3{margin:0 0 10px}
  .logi-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}
  @media(max-width:680px){.logi-grid{grid-template-columns:1fr}}
  .logi h4{margin:0 0 6px;color:var(--green-d);font-size:1rem}
  .logi ul{margin:0;padding-left:18px}
  .logi li{margin:4px 0}

  footer{text-align:center;color:var(--stone);font-size:.85rem;padding:40px 20px 60px}
  footer a{color:var(--stone)}
  .disc{max-width:680px;margin:6px auto 0;font-size:.78rem;opacity:.85}
</style>
</head>
<body>
<header class="hero">
  <div class="kicker">A walking holiday · Lake District</div>
  <h1>Lake&nbsp;District&nbsp;Trek</h1>
  <p class="sub">Six days on foot across the high passes of Cumbria — from Windermere
  to the Irish Sea at Whitehaven, by way of Grasmere, Borrowdale and remote Black Sail.</p>
  <div class="dates">
    <span class="pill">3–10 July 2026</span>
    <span class="pill">__TOTKM__ km walking</span>
    <span class="pill">__WD__ walking days</span>
    <span class="pill">🚆 arrive Fri 3 July, 19:40</span>
    <span class="pill">🚆 depart Fri 10 July, 08:39</span>
  </div>
</header>

<div class="wrap">
  <div class="stats">
    <div class="stat"><b>__TOTKM__</b><span>km on foot</span></div>
    <div class="stat"><b>__TOTASC__</b><span>m of ascent</span></div>
    <div class="stat"><b>__WD__</b><span>walking days</span></div>
    <div class="stat"><b>597</b><span>m · Haystacks</span></div>
  </div>

  <h2 class="section-title">The whole route</h2>
  <p class="section-sub">Each day is colour-coded. Click a line or marker for details.</p>
  <div id="overviewMap"></div>
  <div class="legend" id="legend"></div>

  <h2 class="section-title">Day by day</h2>
  <p class="section-sub">Maps and elevation profiles for every leg.</p>
  <div id="days"></div>

  <div class="logi">
    <h3>Logistics &amp; notes</h3>
    <div class="logi-grid">
      <div>
        <h4>Trains &amp; buses</h4>
        <ul>
          <li>Greg and Mandy arrive Windermere <b>19:40</b>, Fri 3 July.</li>
          <li>Day 6: bus from Scalegill Hall (Bigrigg, A595) to Corkickle / Whitehaven.</li>
          <li>Greg and Mandy return: <b>08:39</b> from Corkickle to Lancaster, <b>Fri 10 July</b>.</li>
          <li>Corkickle station is a 10–15 min walk from Whitehaven harbour.</li>
        </ul>
      </div>
      <div>
        <h4>Good to pack</h4>
        <ul>
          <li>Waterproofs &amp; warm layers — mountain weather changes fast.</li>
          <li>Proper walking boots with ankle support for the passes.</li>
          <li>Cash + snacks: Black Sail is remote with no shops nearby.</li>
          <li>Refillable water bottle; plenty of becks to top up from.</li>
        </ul>
        <h4 style="margin-top:14px">Optional summits from Black Sail</h4>
        <ul>
          <li><b>Haystacks (597 m)</b> — Wainwright’s favourite fell.</li>
          <li><b>Great Gable (899 m)</b> and <b>Pillar (892 m)</b>.</li>
          <li><b>Red Pike (826 m)</b> &amp; <b>Steeple (819 m)</b> ridge.</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<footer>
  <div>Built for a grand walk · maps © OpenStreetMap &amp; OpenTopoMap contributors · routing &amp; elevation by BRouter.</div>
  <p class="disc">Routes follow real OSM hiking paths (BRouter hiking profile); distances, elevation profiles and
  ascent totals come from the routed track. Still indicative — carry OS maps for navigation.</p>
</footer>

<script>
const DATA = __PAYLOAD__;

const topo = () => L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
  {maxZoom:17, attribution:'© OpenTopoMap (CC-BY-SA)'});
const osm  = () => L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  {maxZoom:19, attribution:'© OpenStreetMap'});

// ---------- Overview map ----------
(function(){
  const map = L.map('overviewMap',{scrollWheelZoom:false});
  const base = topo().addTo(map);
  L.control.layers({'Topographic':base,'Street':osm()},null,{position:'topright'}).addTo(map);
  const all=[];
  const legend = document.getElementById('legend');
  DATA.days.forEach(d=>{
    if(!d.geo) return;
    const latlngs = d.geo.coords;
    L.polyline(latlngs,{color:'#ffffff',weight:8,opacity:.9}).addTo(map); // casing for contrast
    L.polyline(latlngs,{color:d.color,weight:4,opacity:1}).addTo(map)
      .bindPopup('<b>'+d.title+'</b><br>'+(d.distance_km?d.distance_km+' km':''));
    if(d.alt_geo){
      L.polyline(d.alt_geo.coords,{color:'#ffffff',weight:7,opacity:.9}).addTo(map);
      L.polyline(d.alt_geo.coords,{color:d.color,weight:3,opacity:1,dashArray:'7 7'}).addTo(map)
        .bindPopup('<b>'+d.title+'</b><br>'+d.alt_label+' (alternative)');
      all.push(...d.alt_geo.coords);
    }
    all.push(...latlngs);
    const start=latlngs[0];
    L.circleMarker(start,{radius:5,color:'#fff',weight:2,fillColor:d.color,fillOpacity:1})
      .addTo(map).bindPopup('<b>'+d.from_to+'</b>');
    const item=document.createElement('span');
    item.innerHTML='<i style="background:'+d.color+'"></i>'+d.title;
    legend.appendChild(item);
  });
  // final destination marker
  const last = DATA.days.filter(d=>d.geo).pop();
  if(last){const end=last.geo.coords[last.geo.coords.length-1];
    L.marker(end).addTo(map).bindPopup('<b>Scalegill Hall</b> · journey’s end — bus to Corkickle / Whitehaven');}
  if(all.length) map.fitBounds(L.latLngBounds(all).pad(0.08));
})();

// ---------- Day cards ----------
const host = document.getElementById('days');
const tpl = (d)=>{
  const badges=[];
  if(d.distance_km) badges.push('<span class="badge">'+d.distance_km+' km</span>');
  if(d.geo){
    badges.push('<span class="badge">↑ '+d.geo.ascent_m+' m</span>');
    badges.push('<span class="badge">↓ '+d.geo.descent_m+' m</span>');
    badges.push('<span class="badge grey">high '+d.geo.max_elev+' m</span>');
  }
  if(d.alt_geo) badges.push('<span class="badge alt">alt ~'+Math.round(d.alt_geo.distance_km)+
      ' km · ↑ '+d.alt_geo.ascent_m+' m</span>');
  if(d.train) badges.unshift('<span class="badge train">🚆 '+d.train+'</span>');
  if(d.kind==='travel') badges.unshift('<span class="badge grey">Travel</span>');
  if(d.kind==='optional') badges.unshift('<span class="badge alt">Optional</span>');
  const linksHtml = d.links.map(l=>'<a href="'+l[1]+'" target="_blank" rel="noopener">'+l[0]+' ↗</a>').join('');
  const stay = d.stay ? '<p class="stay">🏠 <b>Stay:</b> '+
      (d.stay_url?'<a href="'+d.stay_url+'" target="_blank" rel="noopener">'+d.stay+'</a>':d.stay)+'</p>' : '';
  const body = d.geo ? (
      '<div class="day-grid">'+
        '<div><p class="panel-label">Route map</p><div class="map" id="map-'+d.key+'"></div></div>'+
        '<div><p class="panel-label">Elevation profile</p><div class="chartbox"><canvas id="chart-'+d.key+'"></canvas></div></div>'+
      '</div>') : '';
  const numlabel = d.kind==='travel' ? '<small>TRAVEL</small><b>⚑</b>' : '<small>DAY</small><b>'+d.n+'</b>';
  return ''+
  '<div class="day '+(d.kind==='travel'?'travel':'')+'">'+
    '<div class="day-head">'+
      '<div class="daynum" style="background:'+d.color+'">'+numlabel+'</div>'+
      '<div class="h"><div class="date">'+d.date+'</div><h3>'+d.title+'</h3>'+
        '<div class="route">'+d.from_to+'</div></div>'+
      '<div class="badges">'+badges.join('')+'</div>'+
    '</div>'+
    '<div class="day-body">'+
      '<p class="desc">'+d.desc+'</p>'+stay+body+
      (linksHtml?'<div class="links">'+linksHtml+'</div>':'')+
    '</div>'+
  '</div>';
};

DATA.days.forEach(d=>{ host.insertAdjacentHTML('beforeend', tpl(d)); });

// init maps + charts after DOM insert
DATA.days.forEach(d=>{
  if(!d.geo) return;
  const m = L.map('map-'+d.key,{scrollWheelZoom:false});
  topo().addTo(m);
  L.polyline(d.geo.coords,{color:'#ffffff',weight:9,opacity:.9}).addTo(m); // casing
  const line = L.polyline(d.geo.coords,{color:d.color,weight:5,opacity:1}).addTo(m);
  const c=d.geo.coords;
  let bounds = line.getBounds();
  if(d.alt_geo){
    L.polyline(d.alt_geo.coords,{color:'#ffffff',weight:8,opacity:.9}).addTo(m);
    const altLine=L.polyline(d.alt_geo.coords,{color:d.color,weight:4,opacity:1,dashArray:'8 8'})
      .addTo(m).bindTooltip(d.alt_label+' (alternative)');
    bounds = bounds.extend(altLine.getBounds());
  }
  if(d.alt_poi){
    L.circleMarker([d.alt_poi[0],d.alt_poi[1]],{radius:7,color:'#fff',weight:2,fillColor:'#8a4fc2',fillOpacity:1})
      .addTo(m).bindTooltip(d.alt_poi[2]);
  }
  L.circleMarker(c[0],{radius:6,color:'#fff',weight:2,fillColor:'#2f8f4e',fillOpacity:1}).addTo(m).bindTooltip('Start');
  L.circleMarker(c[c.length-1],{radius:6,color:'#fff',weight:2,fillColor:'#c75c3a',fillOpacity:1}).addTo(m).bindTooltip('Finish');
  m.fitBounds(bounds.pad(0.12));

  const toXY=prof=>prof.map(p=>({x:p[0],y:p[1]}));
  const datasets=[{label:d.alt_geo?'Direct route':'Route',data:toXY(d.geo.profile),borderColor:d.color,
      backgroundColor:d.color+'33',fill:true,tension:.3,pointRadius:0,borderWidth:2}];
  if(d.alt_geo) datasets.push({label:d.alt_label,data:toXY(d.alt_geo.profile),borderColor:d.color,
      borderDash:[6,6],fill:false,tension:.3,pointRadius:0,borderWidth:2});
  new Chart(document.getElementById('chart-'+d.key),{
    type:'line',
    data:{datasets},
    options:{responsive:true,maintainAspectRatio:false,animation:false,
      plugins:{legend:{display:!!d.alt_geo},
        tooltip:{callbacks:{title:(i)=>i[0].parsed.x.toFixed(1)+' km',label:(i)=>i.dataset.label+': '+Math.round(i.parsed.y)+' m'}}},
      scales:{
        x:{type:'linear',title:{display:true,text:'Distance (km)'},
           ticks:{maxTicksLimit:7,callback:v=>v}},
        y:{title:{display:true,text:'Elevation (m)'},grid:{color:'#eee'}}}}
  });
});
</script>
</body>
</html>
"""

html = (html
        .replace("__PAYLOAD__", json.dumps(PAYLOAD))
        .replace("__TOTKM__", str(total_km))
        .replace("__TOTASC__", f"{total_ascent:,}")
        .replace("__WD__", str(walk_days)))

with open("index.html", "w") as f:
    f.write(html)
print("WROTE index.html", len(html), "bytes")
print("totals: km=%s ascent=%s walk_days=%s" % (total_km, total_ascent, walk_days))
