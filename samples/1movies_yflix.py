import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://yflix.to/",
    "Accept": "application/json"
}

API = "https://enc-dec.app/api"
YFLIX_AJAX = "https://yflix.to/ajax"

def encrypt(text):
    return requests.get(f"{API}/enc-movies-flix?text={text}").json()["result"]

def decrypt(text):
    return requests.post(f"{API}/dec-movies-flix", json={"text": text}).json()["result"]

def parse_html(html):
    return requests.post(f"{API}/parse-html", json={"text": html}).json()["result"]

def get_json(url):
    return requests.get(url, headers=HEADERS).json()

# 1movies and yflix are the same site with different domains, pick either
# --- Cyberpunk Edgerunners ---
# https://yflix.to/watch/cyberpunk-edgerunners.kmyvry
content_id = "d4K68KU"

# Episodes data
enc_id = encrypt(content_id)
episodes_resp = get_json(f"{YFLIX_AJAX}/episodes/list?id={content_id}&_={enc_id}")
episodes = parse_html(episodes_resp["result"])

# Pick first episode eid to load servers
eid = episodes["1"]["1"]["eid"]
enc_eid = encrypt(eid)
servers_resp = get_json(f"{YFLIX_AJAX}/links/list?eid={eid}&_={enc_eid}")
servers = parse_html(servers_resp["result"])

# Pick first server lid to load embed
lid = servers["default"]["1"]["lid"]
enc_lid = encrypt(lid)
embed_resp = get_json(f"{YFLIX_AJAX}/links/view?id={lid}&_={enc_lid}")
encrypted = embed_resp["result"]

# Decrypt
# Note: subtitles url is passed as urlencoded sub.list parameter
decrypted = decrypt(encrypted)
print(f"\n{'-'*25} Decrypted Data {'-'*25}\n")
print(decrypted)
