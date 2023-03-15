# -*- coding: utf-8 -*-
# @Time     : 2018/10/08 
# @Author   : liguibin
#

###
'''
usage: xmlyMp3Dl.py [-h] [-o OUTPUT] [-v] [-n] url

download all audioes in ximalay album like
:https://www.ximalaya.com/ertong/11106118

positional arguments:
  url                   web url need to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
  -v, --verbosity       increase output verbosity
  -n, --noIndex         not add index to prefix
'''

import os
import re
import sys
import json
import copy
import requests
import argparse
import subprocess
# from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    }

defaultOutputFile = 'dl_xmly.sh'

defaultAlbumUrl = 'https://www.ximalaya.com/ertong/11106118'

#albumId=3533672(aId), pageNum=1(pNum)
fetchUrlModel = 'https://www.ximalaya.com/revision/play/album?albumId=aId&pageNum=pNum&sort=-1&pageSize=30'


def get_song_info_list(album_id=3533672, page_size=30):
    print("## get_song_info_list")
    song_info_list = []
    song_info = {}
    for page in range(1, 20):
        url = f'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={album_id}&pageNum={page}&sort=1&pageSize={page_size}'
        res = requests.get(url=url, headers=headers)
        print(url)
        jsonData = json.loads(res.text)
        tracks_list = jsonData['data']['tracks']
        if tracks_list:
            for track in tracks_list:
                # print(track)
                idx = track['index']
                title = track['title']
                song_info["trackId"] = track['trackId']
                song_info["name"] = f"p{idx:03d}_{title}"
                song_info_list.append(copy.deepcopy(song_info))

    return song_info_list

def get_audio_url_list(song_info_list):
    print("## get_audio_url_list")
    for info in song_info_list:
        audio_info_url = f"https://www.ximalaya.com/revision/play/v1/audio?id={info['trackId']}&ptype=1"
        res = requests.get(url=audio_info_url, headers=headers)
        print(audio_info_url)
    #     print(res.text)
        jsonData = json.loads(res.text)
        if jsonData["ret"] != 200:
            continue
        if "src" in jsonData["data"]:
            info['audio_url'] = jsonData["data"]["src"]    

    return song_info_list

def get_download_sh(song_info_list, filename="./dl.sh"):
    with open(filename, mode='w') as f:
        for info in song_info_list:
            song_name = info['name'].replace("-","_").replace(" ","").replace("(","[").replace(")","]")
            if "audio_url" in info:
                wget_str = f"wget -O {song_name}.m4a {info['audio_url']}\n"
                print(wget_str)
                f.write(wget_str)
        ffmpeg_str = 'for i in *.m4a; do ffmpeg -i "$i" "${i%.*}.mp3"; done '
        f.write(ffmpeg_str)
    print(f"save file to {filename}")


def main(albumUrl, outputFile):
    # extract number from string
    albumIdStr = re.findall('\d+', albumUrl)[0]
    song_info_list = get_song_info_list(album_id=albumIdStr, page_size=30)
    song_info_list = get_audio_url_list(song_info_list)
    get_download_sh(song_info_list, filename=outputFile)

    p = subprocess.Popen(["chmod", "+x", outputFile], stdout=subprocess.PIPE)
    print('\n for i in *.m4a; do ffmpeg -i "$i" "${i%.*}.mp3"; done \n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download all audioes in ximalay album like :' + defaultAlbumUrl)
    parser.add_argument('url', type=str, help="web url need to download")
    parser.add_argument("-o", "--output", default='./dl.sh', help="output file name")

    args = parser.parse_args()
    webUrl = args.url
    outputFile = args.output

    main(webUrl, outputFile)
