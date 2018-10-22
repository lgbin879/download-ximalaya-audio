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
import requests
import argparse
import subprocess
from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    }

defaultOutputFile = 'dl_xmly.sh'

defaultAlbumUrl = 'https://www.ximalaya.com/ertong/11106118'

#albumId=3533672(aId), pageNum=1(pNum)
fetchUrlModel = 'https://www.ximalaya.com/revision/play/album?albumId=aId&pageNum=pNum&sort=-1&pageSize=30'


def main(albumUrl, outputFile, noIndex, pageList):
    f = open(outputFile, 'w+')

    res = requests.get(albumUrl, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # extract number from string
    albumIdStr = re.findall('\d+', albumUrl)[0]
    songNum = int(re.findall('\d+', soup.findAll('h2')[0].text)[0])

    if len(pageList) == 0:
        if len(soup.findAll('input', attrs={'class': 'control-input'})):
            pageNum = int(soup.findAll('input', attrs={'class': 'control-input'})[0]['max'])
        else:
            pageNum = 1

        pList = range(1, pageNum+1)
        print("## Info : albumIdStr = %s, pageNum = %d, songNum = %d" %(albumIdStr, pageNum, songNum))
    else:
        pList = pageList
    
    for i in pList:
        i = int(i)
        pageUrl = albumUrl+r'/p'+str(i)
        fetchUrl = fetchUrlModel.replace('aId', albumIdStr).replace('pNum', str(i))
        resPage = requests.get(fetchUrl, headers=headers)

        if resPage.status_code == 200:
            print('\n## Info : Success get %s\n' %(fetchUrl))
        else:
            sys.exit('\n## Error : Error while getting %s\n' %(fetchUrl))

        msgJson = json.loads(resPage.text)
        pageSize = len(msgJson['data']['tracksAudioPlay']) 

        for j in range(0, pageSize):
            title = msgJson['data']['tracksAudioPlay'][j]['trackName'].replace(' ', '')
            idx = int(msgJson['data']['tracksAudioPlay'][j]['index'])

            index = idx #songNum - pageSize*i + idx - pageSize*(i-1)
            m4aUrl = msgJson['data']['tracksAudioPlay'][j]['src']

            prefix = "{:0>3}".format(str(index))+'_'
            fileName = title+'.mp3'

            if not noIndex:
            	fileName = prefix+fileName

            print('wget -O ', fileName, m4aUrl)
            print('wget -O ', fileName, m4aUrl, file=f)


    f.close()
    p = subprocess.Popen(["chmod", "+x", outputFile], stdout=subprocess.PIPE)
    print('\n## Info : save result to excutable file : ' + outputFile)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download all audioes in ximalay album like :' + defaultAlbumUrl)
    parser.add_argument('url', type=str, help="web url need to download")
    parser.add_argument("-o", "--output", help="output file name")
    parser.add_argument("-p", "--page", help="specify page need to download")
    parser.add_argument("-n", "--noIndex", help="not add index to prefix", action="store_true")
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")

    args = parser.parse_args()
    webUrl = args.url
    outputFile = args.output
    noIndex = False

    # input url format checker
    if os.path.isfile(webUrl):
        pass
    elif re.match(r'http[s]?://www.ximalaya.com/\w+/\d+', webUrl):
        pass
    else:
    	sys.exit('\n ## Error : unrecognize url, please input correct url format like : ' + defaultAlbumUrl)

    if args.output:
    	outputFile = args.output
    else:
        print('## Info : save result to default File : ', defaultOutputFile)
        outputFile = defaultOutputFile

    charList=[',', '.',  r'/', r'\\']
    if args.page:
        pageList = list(args.page)
        for p in pageList:
            if p in charList:
                pageList.remove(p)
            else:
                p = int(p)

        print('download pages in'+str(pageList))
    else:
        pageList = []

    if args.noIndex:
    	print("## Info : don't add index to prefix")
    	noIndex = True

    main(webUrl, outputFile, noIndex, pageList)
