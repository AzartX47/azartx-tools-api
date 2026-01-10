import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://animekai.to/",
    "Accept": "application/json"
}

API = "https://enc-dec.app/api"
DATABASE = "https://enc-dec.app/db"
KAI_AJAX = "https://animekai.to/ajax"

def encrypt(text):
    return requests.get(f"{API}/enc-kai?text={text}").json()["result"]

def decrypt(text):
    return requests.post(f"{API}/dec-kai", json={"text": text}).json()["result"]

def parse_html(html):
    return requests.post(f"{API}/parse-html", json={"text": html}).json()["result"]

def get_json(url):
    return requests.get(url, headers=HEADERS).json()

'''
--- Database Functions ---

Statistics: https://enc-dec.app/api/db/kai/

Search database by ID: kai_id, mal_id, or anilist_id
    - Example: https://enc-dec.app/api/db/kai/find?mal_id=42310
Search by title query (optional: type, year)
    - Example: https://enc-dec.app/api/db/kai/search?query=cyberpunk&type=tv&year=2022
'''

# --- Cyberpunk Edgerunners ---
# https://myanimelist.net/anime/42310/Cyberpunk__Edgerunners
mal_id = "42310"

# Query database by mal_id
entries = requests.get(f"{DATABASE}/kai/find?mal_id={mal_id}").json()

# Pull episodes from first result in list.
# If doing imprecise search, muliple items may be returned.
# 'episodes' field contains titles under 'title' key, and episode tokens under 'token' key.
episodes = entries[0]["episodes"]

# Pick first episode token to load servers
token = episodes["1"]["1"]["token"]
enc_token = encrypt(token)
servers_resp = get_json(f"{KAI_AJAX}/links/list?token={token}&_={enc_token}")
servers = parse_html(servers_resp["result"])

# Pick first server lid to load embed
lid = servers["sub"]["1"]["lid"]
enc_lid = encrypt(lid)
embed_resp = get_json(f"{KAI_AJAX}/links/view?id={lid}&_={enc_lid}")
encrypted = embed_resp["result"]

# Decrypt
decrypted = decrypt(encrypted)
print(f"\n{'-'*25} Decrypted Data {'-'*25}\n")
print(decrypted)
