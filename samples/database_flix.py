import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Connection": "keep-alive"
}

API = "https://enc-dec.app/api"
DATABASE = "https://enc-dec.app/db"
YFLIX_AJAX = "https://yflix.to/ajax"

def encrypt(text):
    return requests.get(f"{API}/enc-movies-flix?text={text}").json()["result"]

def decrypt(text):
    return requests.post(f"{API}/dec-movies-flix", json={"text": text}).json()["result"]

def parse_html(html):
    return requests.post(f"{API}/parse-html", json={"text": html}).json()["result"]

def get_json(url):
    return requests.get(url, headers=HEADERS).json()

'''
--- Database Functions ---

Statistics: https://enc-dec.app/api/db/flix/

Search database by ID: tmdb_id, imdb_id, or flix_id (optional: type)
    - Example: https://enc-dec.app/db/flix/find?tmdb_id=1399&type=tv
Search by title query (optional: type, year)
    - Example: https://enc-dec.app/db/flix/search?query=game+of+thrones&type=tv&year=2011
'''

# --- Game Of Thrones ---
# https://www.themoviedb.org/tv/1399-game-of-thrones
tmdb_id = "1399"

# Query database by tmdb_id
entries = requests.get(f"{DATABASE}/flix/find?tmdb_id={tmdb_id}").json()

# Pull episodes from first result in list.
# If doing imprecise search, muliple items may be returned.
# 'episodes' field contains titles under 'title' key, and episode eids under 'eid' key.
episodes = entries[0]["episodes"]

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
