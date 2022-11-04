import argparse
import uuid

from src.mediaRepository import MediaRepository
from src.publisher import Publisher
from src.subscriber import Subscriber
from src.downloader import list_subtitles, download_subtitle


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

## read data from repository
media = mediaRepository.read_media(id)

## process data
url = media["config"]["url"]

subtitles = list_subtitles(url)
print(subtitles)

for lang in subtitles['subtitles']:
    print("available formats",lang,subtitles['subtitles'][lang])
    vtt = download_subtitle(url,lang, "vtt")
    print("vtt",len(vtt))
    
    ## update repository
    subtitle = {
        "id" : str(uuid.uuid4()),
        "media_id" : media["id"],
        "language" : lang,
        "format" : "vtt",
        "data" : vtt
    }
    mediaRepository.create_subtitle(subtitle)
    ## publish change message
    publisher.publish("/db/subtitle/create",{ "id" : subtitle["id"] })



