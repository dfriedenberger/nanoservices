import youtube_dl
import urllib.request 
import requests

def list_metadata(url):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            url,
            download=False # We just want to extract the info
        )

    return result

def list_subtitles(url):
    result = {}
    metadata = list_metadata(url)
    result["subtitles"] = {}
    for k in metadata['subtitles']:
        extensions = []
        for st in metadata['subtitles'][k]:
            extensions.append(st['ext']) #,st['url'])
        result["subtitles"][k] = extensions
    result["url"] = url
    return result




def download_subtitle(url,subtitle,ext):

    metadata = list_metadata(url)
    for st in metadata['subtitles'][subtitle]:
        if st['ext'] != ext: continue
        with urllib.request.urlopen(st['url']) as h:
            return h.read()
    
    raise ValueError("format {} not found in subtitles ".format(ext))


