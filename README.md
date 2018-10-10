# download-ximalaya-audio

下载喜马拉雅FM专辑中所有音频

用法：
python3 xmlyMp3Dl.py https://www.ximalaya.com/ertong/3533672/

得到一个dl_xmly.sh文件，获取专辑中音频url并正确命名：
wget -O  001_夏影.mp3 http://audio.xmcdn.com/group11/M08/94/4D/wKgDa1ZM6ebz1zZFABp396pn0rA557.m4a

执行 dl_xmly.sh，将所有音频下载到本地：
sh dl_xmly.sh

注意！！仅支持python3，Python2请自行修改

更多参数用法请参考：
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
