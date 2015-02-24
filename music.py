import vk
import argparse
import VkAuth
import sys
import time
import tempfile
import threading
from enum import Enum
from urllib import request
import re
from pyglet import media


class MusPlayer:
    def __init__(self):
        self.song_ = media.Source
        self.volume_ = 1.0
        self.paused = False
        self.player_ = media.Player()

    def launch(self, song):
        self.paused = False
        self.song_ = media.load(filename=song)
        for num in range(10, 0, -1):
            self.set_volume(num/10.0)
            time.sleep(0.05)

        self.player_.queue(self.song_)
        self.player_.play()
        if self.player_.time != 0:
            self.forward(0)
        self.set_volume(1.0)

    def set_volume(self, volume):
        if 0.0 <= volume <= 1.0:
            self.volume_ = volume
            self.player_.volume = self.volume_

    def pause(self):
        if self.paused:
            self.player_.play()
        else:
            self.player_.pause()
        self.paused = not self.paused

    def stop(self):
        self.player_.pause()

    def forward(self, val):
        if 0.0 <= val <= 1.0:
            seek_to = self.song_.duration * val
            self.player_.seek(seek_to)

class Commands(Enum):
    PLAY = 'play'
    VOL = 'vol'
    PAUSE = 'pause'
    EXIT = 'exit'
    TIME = 'time'

class VKMusic:

    def __init__(self, connect_cb, disconnect_cb, newSong_cb, pause_cb):
        self.tag = '#'
        self.login = ''
        self.password = ''
        self.player = MusPlayer()
        self.doConnect = False
        self.running = False
        self.connected = False
        self.t = threading.Thread(target=self.worker)
        self.t.daemon = True
        self.exit = ''
        self.connectCallback = connect_cb
        self.disconnectCallback = disconnect_cb
        self.newSongCallback = newSong_cb
        self.pauseCallback = pause_cb

    def get_token(self):
        token, id = VkAuth.auth(self.login, self.password, '4545547', 'messages,audio')

        return token, id

    def connect(self, login, password):
        self.start_worker()
        self.login = login
        self.password = password
        self.doConnect = True


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
    def temp_download_from(url):
        r = request.urlopen(url)
        data = r.read()
        f = tempfile.SpooledTemporaryFile()
        f.write(data)
        return f

    @staticmethod
    def isint(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def start_worker(self):
        if not self.running:
            self.t.start()
            self.running = True

    def stop_worker(self):
        self.exit = 'exit'

    def worker(self):
        while not self.connected:
            if self.doConnect:
                try:
                    token, user_id = self.get_token()
                    vkapi = vk.API(access_token=token)
                    self.connectCallback()
                    self.connected = True
                except:
                    self.disconnectCallback("Something went wrong. Check login and password")
                    self.doConnect = False
            else:
                time.sleep(0.5)

        a = 1
        while self.exit is '':
            try:
                messages = vkapi.messages.getHistory(user_id=user_id, count='1')
                command = messages['items'][0]['body']
                if self.is_command(command):
                    command_type, command = self.extract_command(command)
                    if command_type == Commands.PLAY.value:
                        audio = vkapi.audio.search(q=command, count='1')['items'][0]['url']

                        mp3_song = self.download_from(audio)
                        self.player.launch(mp3_song)
                        a += 1
                    elif command_type == Commands.PAUSE.value:
                        self.player.pause()
                    elif command_type == Commands.VOL.value:
                        if VKMusic.isint(command):
                            self.player.set_volume(float(command)/100)
                    elif command_type == Commands.TIME.value:
                        if VKMusic.isint(command):
                            self.player.forward(float(command)/100)

                    vkapi.messages.delete(message_ids=messages['items'][0]['id'])
                else:
                    time.sleep(1)
            except:
                #vkapi.messages.send(user_id=user_id, guid=a, message='Exception occured: ' + str(sys.exc_info()[0]) + str(a))
                print(str(sys.exc_info()[0]))
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VKMusic remote player')
    parser.add_argument('login', help='Your vk login')
    parser.add_argument('password', help='Your vk password')

    args = parser.parse_args()

    mus = VKMusic(args.login, args.password)
    mus.worker()
