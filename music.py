import vk
import argparse
import sys
import time
import tempfile
import threading
from enum import Enum
from urllib import request
from requests.exceptions import RequestException
import json
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

    def __init__(self, connect_cb, disconnect_cb, newSong_cb, pause_cb, debug=False):
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
        self.debug = debug
        self.vkapi = None
        self.user_id = ''

    def connect(self, login, password):
        if not self.debug:
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

    def connect_to_longpoll(self):
        try:
            server_info = self.vkapi.messages.getLongPollServer(use_ssl='1', need_pt='1')
            print('Connected to longPoll server: ' + server_info['server'])
            return server_info
        except RequestException as e:
            print('Failed to connect to longPoll Server. Reason: {}' + e)
            return None

    def exec_command(self, command):
        command_type, command['text'] = self.extract_command(command['text'])
        if command_type == Commands.PLAY.value:
            audio = self.vkapi.audio.search(q=command['text'], count='1')['items'][0]['url']
            mp3_song = self.download_from(audio)
            self.player.launch(mp3_song)
        elif command_type == Commands.PAUSE.value:
            self.player.pause()
        elif command_type == Commands.VOL.value:
            if VKMusic.isint(command['text']):
                self.player.set_volume(float(command['text'])/100)
        elif command_type == Commands.TIME.value:
            if VKMusic.isint(command['text']):
                self.player.forward(float(command['text'])/100)
        elif command_type == Commands.EXIT.value:
            self.exit = 'exit'
        self.vkapi.messages.delete(message_ids=command['id'])

    def worker(self):
        while not self.connected:
            if self.doConnect:
                try:
                    self.vkapi = vk.API(user_login=self.login,user_password=self.password, app_id='4545547', scope='messages,audio', timeout=5)
                    self.user_id = self.vkapi.users.get()[0]['id'];
                    if self.connectCallback is not None:
                        self.connectCallback()
                    self.connected = True
                    print('Successfully connected. UserId = ' + str(self.user_id))
                except:
                    if self.disconnectCallback is not None:
                        self.disconnectCallback("Something went wrong. Check login and password")
                    print('Failed to connect')
                    self.doConnect = False
            else:
                time.sleep(0.5)

        attempts = 5
        ts = 0
        server_info = None
        while attempts != 0 and server_info is None:
            server_info = self.connect_to_longpoll()
            attempts -= 1

        if server_info is None:
            print('Ran out of attempts to establish a connection with longPoll server. Exiting')
            self.exit = 'exit'
        else:
            ts = server_info['ts']

        query = 'https://{}?act=a_check&key={}&ts={}&wait=25&mode=2'
        while self.exit is '':
            try:
                messages = []
                res = request.urlopen(query.format(server_info['server'], server_info['key'], ts))
                updates = json.loads(res.read().decode('utf-8'))
                ts = updates['ts']
                for update in updates['updates']:
                    if len(update) > 3 and update[0] == 4 and update[3] == int(self.user_id):
                        messages.append({'text': update[6], 'id': update[1]})
                        print('Received new message: ' + update[6])

                for message in messages:
                    if self.is_command(message['text']):
                        self.exec_command(message)

            except ValueError as e:
                print(e)
            except:
                #vkapi.messages.send(user_id=user_id, guid=error, message='Exception occured: ' + str(sys.exc_info()[0]) + str(error))
                print(str(sys.exc_info()[0]))
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VKMusic remote player')
    parser.add_argument('login', help='Your vk login')
    parser.add_argument('password', help='Your vk password')

    args = parser.parse_args()

    mus = VKMusic(None, None, None, None, True)
    mus.connect(args.login, args.password)
    mus.worker()
