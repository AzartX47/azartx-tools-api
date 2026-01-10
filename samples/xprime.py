import requests
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Origin": "https://xprime.tv",
    "Referer": "https://xprime.tv"
}

API = "https://enc-dec.app/api"

# --- XPrime is currently disabled ---

# Note that there are different servers, find them here: https://backend.xprime.tv/servers
# Movie format: <https://backend.xprime.tv/{server}?name={title}&year={year}&id={tmdb_id}&imdb={imdb_id}>
# Tv format: <https://backend.xprime.tv/{server}?name={title}&year={year}&id={tmdb_id}&imdb={imdb_id}&season={season_number}&episode={episode_number}>

# --- Cyberpunk Edgerunners ---
title = "Cyberpunk: Edgerunners"
type = "tv"
year = "2022"
imdb_id = "tt12590266"
tmdb_id = "105248"
season = "1"
episode = "1"

# Generate turnstile token
token = requests.get(f"{API}/enc-xprime").json()['result']

# Get encrypted text
url = f"https://backend.xprime.tv/primebox?name={quote(title)}&year={year}&id={tmdb_id}&imdb={imdb_id}&season={season}&episode={episode}&turnstile={token}"
encrypted = requests.get(url, headers=HEADERS).text

# Decrypt
decrypted = requests.post(f"{API}/dec-xprime", json={"text": encrypted}).json()['result']
print(f"\n{'-'*25} Decrypted Data {'-'*25}\n")
print(decrypted)
