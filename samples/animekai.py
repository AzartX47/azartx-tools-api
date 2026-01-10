import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Referer": "https://animekai.to/",
    "Accept": "application/json"
}

API = "https://enc-dec.app/api"
KAI_AJAX = "https://animekai.to/ajax"

def encrypt(text):
    return requests.get(f"{API}/enc-kai?text={text}").json()["result"]

def decrypt(text):
    return requests.post(f"{API}/dec-kai", json={"text": text}).json()["result"]

def parse_html(html):
    return requests.post(f"{API}/parse-html", json={"text": html}).json()["result"]

def get_json(url):
    return requests.get(url, headers=HEADERS).json()

# --- Cyberpunk Edgerunners ---
# https://animekai.to/watch/cyberpunk-edgerunners-x6qm
content_id = "c4G-8K8"

# Episodes data
enc_id = encrypt(content_id)
episodes_resp = get_json(f"{KAI_AJAX}/episodes/list?ani_id={content_id}&_={enc_id}")
episodes = parse_html(episodes_resp["result"])

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
