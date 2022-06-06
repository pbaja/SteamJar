from typing import List
from dataclasses import dataclass
import urllib.request
import urllib.parse
import urllib.error
import json, logging

BASE_URL = 'https://www.steamgriddb.com/api/v2'
API_KEY = '40e71625bff0718ebd25ebc459771543'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'

@dataclass
class SearchResult:
    id: int
    name: str
    types: List[str]
    verified: bool
    release_date: str = ''

def request(api_path):
    req = urllib.request.Request(BASE_URL + api_path)
    req.add_header('Authorization', f'Bearer {API_KEY}')
    req.add_header('User-Agent', USER_AGENT)
    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            if response_data.get('success', False):
                return response_data['data']
    except urllib.error.HTTPError as e:
        logging.error(f'HTTPError {e.code}: {e.read().decode()}')
        return []

def download(file_url, file_path):
    req = urllib.request.Request(file_url)
    req.add_header('Accept', '*/*')
    req.add_header('User-Agent', USER_AGENT)
    try:
        with urllib.request.urlopen(req) as response:
            with file_path.open('wb') as f:
                f.write(response.read())
    except urllib.error.HTTPError as e:
        logging.error(f'HTTPError {file_url}: {e}')

def search(term):
    data = request(f'/search/autocomplete/{urllib.parse.quote_plus(term)}')
    return [SearchResult(**item) for item in data]

def download_grid(game_id, file_path):
    data = request(f'/grids/game/{game_id}')
    if len(data) > 0:
        file_url = data[0]['url']
        download(file_url, file_path)

def download_logo(game_id, file_path):
    data = request(f'/logos/game/{game_id}')
    if len(data) > 0:
        file_url = data[0]['url']
        download(file_url, file_path)

def download_hero(game_id, file_path):
    data = request(f'/heroes/game/{game_id}')
    if len(data) > 0:
        file_url = data[0]['url']
        download(file_url, file_path)