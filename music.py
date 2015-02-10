import vk
import argparse
import sys
import time
from enum import Enum
from urllib import parse, request
import re
from selenium import webdriver
import pydub
from pygame import mixer


class MusPlayer:
    def __init__(self):
        self.song = ''
        self.volume_ = 1.0
        self.paused = False
        mixer.init()

    def launch(self, song):
        self.paused = False
        mixer.music.load(song)
        mixer.music.play()
        mixer.music.set_volume(self.volume_)

    def set_volume(self, volume):
        if 0.0 <= volume <= 1.0:
            self.volume_ = volume
            mixer.music.set_volume(self.volume_)

    def pause(self):
        if self.paused:
            mixer.music.unpause()
        else:
            mixer.music.pause()
        self.paused = not self.paused

    def stop(self):
        mixer.music.stop()

    def forward(self, val):
        mixer.music.set_pos(val)

class Commands(Enum):
    PLAY = 'play'
    VOL = 'vol'
    PAUSE = 'pause'
    EXIT = 'exit'
    TIME = 'time'

class VKMusic:

    def __init__(self, login, password):
        self.tag = '#'
        self.login = login
        self.password = password
        pydub.AudioSegment.converter = "c:/users/chup/desktop/ffmpeg.exe"
        self.player = MusPlayer()

    def get_token(self):
        driver = webdriver.Firefox()

        parameters = {
            'client_id': 4545547,
            'scope': 'messages,audio',
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'response_type': 'token',
        }

        driver.get(r"http://api.vkontakte.ru/oauth/authorize?%s" % parse.urlencode(parameters))

        user_input = driver.find_element_by_name("email")
        user_input.send_keys(self.login)
        password_input = driver.find_element_by_name("pass")
        password_input.send_keys(self.password)

        submit = driver.find_element_by_id("install_allow")
        submit.click()

        result_link = driver.current_url
        driver.close()

        token = re.search('access_token=([0-9A-Za-z]+)&', result_link).group(1)
        id = re.search('user_id=([0-9A-Za-z]+)', result_link).group(1)

        return token, id

    def extract_command(self, cmd_string):
        a = re.search('(' + self.tag + ')([0-9A-Za-z]+)', cmd_string)
        cmd_type = a.group(2)
        body = cmd_string[a.end() + 1:]
        return cmd_type, body

    def is_command(self, cmd):
        if self.tag in cmd:
            return True
        return False

    @staticmethod
    def download_from(url):
        r = request.urlopen(url)
        data = r.read()
        with open('temp.mp3', 'w+b') as f:
            f.write(data)
            f.flush()
        return 'temp.mp3'

    @staticmethod
    def isint(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def worker(self):
        token, user_id = self.get_token()
        vkapi = vk.API(access_token=token)

        exit = ''
        a = 1
        while exit is '':
            try:
                messages = vkapi.messages.getHistory(user_id=user_id, count = '1')
                command = messages['items'][0]['body']
                if self.is_command(command):
                    command_type, command = self.extract_command(command)
                    if command_type == Commands.PLAY.value:
                        audio = vkapi.audio.search(q=command, count='1')['items'][0]['url']

                        mp3_song = self.download_from(audio)
                        #with open(mp3_song.name, 'rb') as sng:
                        audio = pydub.AudioSegment.from_mp3(mp3_song)
                        self.player.stop()
                        audio.export('temp{0}.wav'.format(a), format='wav')
                        self.player.launch('temp{0}.wav'.format(a))
                        a += 1
                    elif command_type == Commands.PAUSE.value:
                        self.player.pause()
                    elif command_type == Commands.VOL.value:
                        if VKMusic.isint(command):
                            self.player.set_volume(float(command)/100)
                    elif command_type == Commands.TIME.value:
                        if VKMusic.isint(command):
                            self.player.forward(float(command)/50)
                        pass

                    vkapi.messages.delete(message_ids=messages['items'][0]['id'])
                else:
                    time.sleep(1)
            except:
                vkapi.messages.send(user_id=user_id, guid=a, message='Exception occured: ' + str(sys.exc_info()[0]) + str(a))
                a += 1
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VKMusic remote player')
    parser.add_argument('login', help='Your vk login')
    parser.add_argument('password', help='Your vk password')

    args = parser.parse_args()

    mus = VKMusic(args.login, args.password)
    mus.worker()