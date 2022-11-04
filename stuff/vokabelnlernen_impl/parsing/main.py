import argparse

from src.mediaRepository import MediaRepository
from src.publisher import Publisher
from src.subscriber import Subscriber

import webvtt
from io import StringIO

import requests
import urllib.parse

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='{description}')
    parser.add_argument("--id", required=True, metavar="ID", help="Object Id for operation")
    args = parser.parse_args()
    return args.id



mediaRepository = MediaRepository()
publisher = Publisher()
subscriber = Subscriber()



id = parse_args()
print("id",id) 

#Implementation

url = 'https://text.frittenburger.de/parse'
headers = {
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Authorization' : 'Bearer limited-guest-access'}


languages = {
    "en" : "english",
    "es" : "spanish",
    "de" : "german"
}
## read data from repository
subtitle = mediaRepository.read_subtitle(id)

if subtitle['format'] != 'vtt':
    raise ValueError(f"Only can parse vtt not {subtitle['format']}")
lk = subtitle['language']
language = languages[lk]

buffer = StringIO(subtitle['data'])

## process data

for caption in webvtt.read_buffer(buffer):
    print(caption.start)
    print(caption.end)
    print(caption.text)

    text = caption.text

    payload = 'language=' + language+'&text=' + urllib.parse.quote(text)
    r = requests.post(url, data=payload, headers=headers,verify=False)
    print(r.status_code,r.reason)
    result = r.json()
    for sentence in result['text']['sentences']:
        print("text", sentence['text'])
        print("tokens",sentence['tokens'])



## update repository

## publish change message

