#!/usr/bin/env python3

import os
import sys
from sh import sensors
from time import sleep
from tempfile import mktemp
from urllib.request import build_opener

# Speak params.
mp3 = mktemp()
opener = build_opener()
google_translate_url = 'http://translate.google.com/translate_tts'
agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'
opener.addheaders = [('User-agent', agent)]


def parse_temps(line):
    cut = slice(1, 5)
    return float(line.split(':')[1].strip()[cut])


def get_temps():
    res = sensors()
    lines = res.stdout.decode(encoding='UTF-8').split('\n')
    temps = []
    for line in lines:
        if 'Core' in line:
            temps.append(parse_temps(line))
    return max(temps)


def speak(phrase):
    try:
        url = phrase.replace(' ', '%20')
        response = opener.open('%s?q=%s&tl=en' %
                               (google_translate_url, url))
        ofp = open(mp3, 'wb')
        ofp.write(response.read())
        ofp.close()
        os.system('mplayer2 %s > /dev/null 2>&1' % mp3)
    except:
        os.system('espeak "%s"' % phrase)
    return None

def main():
    while True:
        sleep(2)
        os.system('clear && sensors')
        temp = get_temps()
        phrase = None
        if temp >= 94:
            phrase = 'Temperature is %s' % temp
        if temp > 96:
            phrase = 'Turn off the computer before it blows up!'

        if phrase:
            speak(phrase)
            sleep(1)

if __name__ == '__main__':
    sys.exit(main())
