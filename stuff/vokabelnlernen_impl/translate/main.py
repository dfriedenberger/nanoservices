import argparse

from src.mediaRepository import MediaRepository


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='{description}')
    parser.add_argument("--id", required=True, metavar="ID", help="Object Id for operation")
    args = parser.parse_args()
    return args.id



mediaRepository = MediaRepository()



id = parse_args()
print("id",id) 

#Implementation

## read data from repository

## process data

## update repository

## publish change message

