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
out = {"maj": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "src": "Steam : annonces officielles d'AION 2", "items": items}
old = None
try:
    old = json.load(open("news-auto.json"))
except Exception:
    pass
if old and old.get("items") == items:
    print("rien de nouveau")
else:
    json.dump(out, open("news-auto.json", "w"), ensure_ascii=False, indent=1)
    print("mis à jour :", len(items), "annonces")
