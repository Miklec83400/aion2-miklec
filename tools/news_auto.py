# Récupère les dernières annonces officielles d'AION 2 sur Steam (API publique) et les écrit dans news-auto.json.
import json, urllib.request, datetime, re, html
URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3393110&count=15&maxlength=300&format=json"
with urllib.request.urlopen(URL, timeout=30) as r:
    data = json.load(r)
items = []
for it in data.get("appnews", {}).get("newsitems", []):
    if it.get("feedname") not in ("steam_community_announcements",):
        continue
    txt = re.sub(r"\[[^\]]*\]|<[^>]+>|\{STEAM_CLAN_IMAGE\}\S*", " ", it.get("contents", ""))
    txt = html.unescape(re.sub(r"\s+", " ", txt)).strip()
    items.append({"t": it.get("title", ""), "u": it.get("url", ""), "d": it.get("date", 0), "x": txt[:240]})
items = items[:10]
fr = []
try:
    import xml.etree.ElementTree as ET
    req = urllib.request.Request("https://www.ateliergaming.fr/feed/", headers={"User-Agent": "Mozilla/5.0 (aion2-miklec news bot)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    import email.utils
    for it in root.iter("item"):
        t = (it.findtext("title") or "").strip()
        if "aion" not in t.lower():
            continue
        d = it.findtext("pubDate") or ""
        try:
            ts = int(email.utils.parsedate_to_datetime(d).timestamp())
        except Exception:
            ts = 0
        fr.append({"t": html.unescape(t), "u": (it.findtext("link") or "").strip(), "d": ts, "x": ""})
except Exception as e:
    print("Atelier Gaming : non lu", e)
fr = fr[:8]
out = {"maj": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "src": "Steam : annonces officielles d'AION 2", "items": items, "fr": fr}
old = None
try:
    old = json.load(open("news-auto.json"))
except Exception:
    pass
if old and old.get("items") == items and old.get("fr") == fr:
    print("rien de nouveau")
else:
    json.dump(out, open("news-auto.json", "w"), ensure_ascii=False, indent=1)
    print("mis à jour :", len(items), "annonces")
