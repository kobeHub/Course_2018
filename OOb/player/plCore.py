#!/usr/bin/python3
"""
对core类的实现，作为音频播放的主体类
控制音频的加载，播放，快进，快退

"""
import pyglet
import os.path
import time
from pyglet.window import key

from core import *
from pydub import AudioSegment



class AudioPlayer(playCore):
    def __init__(self):
        super(AudioPlayer, self).__init__()
        self.player = pyglet.media.Player()
        self.media = None
        self.song_time = 0
        self.play_list = []
        self.current_playing = 0
        self.status_types = ["init", "paused", "playing", "eof"]
        self.status = self.status_types[0]
        self.volume = 0.5
        self.paused_flag = 1
    
    def play(self):
        print(self.status)
        if self.status == self.status_types[1]:
            self.player.play()
        else:
            self.stop()

            self.set_volume(self.volume)

            print(self.get_current_play_list_item())
            self.load(self.get_current_play_list_item())
            self.player = pyglet.media.Player()
            self.player.queue(self.media)
            self.player.play()

        if self.is_playing():
            self.status = self.status_types[2]
        else:
            self.status = self.status_types[0]

    def play_next(self):
        if len(self.play_list) != self.current_playing+1:
            self.current_playing += 1
            self.play()

    def play_previous(self):
        if self.current_playing != 0:
            self.current_playing -= 1
            self.play()

    def load(self, uri):
        try:
            self.media = pyglet.media.load(uri)
            raw = AudioSegment.from_file(uri)
            self.duration = int(len(raw)/1000) + 1
            print('Name:', os.path.basename(uri))
            print('Dur:{0}s'.format(self.duration))
        except Exception as e:
            print('Load error: ', repr(e))

    def pause(self):
        print('[+]paused')
        self.player.pause()
        self.status = self.status_types[1]

    def stop(self):
        self.player.pause()
        self.status = self.status_types[0]
        self.player.delete()
        self.media = None

    def seek(self, position):
        self.player.seek(position)

    def set_volume(self, value):
        self.volume = value
        self.player.volume = value

    def get_duration(self):
        return str(self.duration//60)+':'+str(self.duration%60)

    def get_volume(self):
        return self.player.volume

    def get_current_time(self):
        return self.player.time

    def is_media_loaded(self):
        return self.media is not None

    def is_playing(self):
        return self.player.playing

    def is_play_list_end(self):
        return self.current_playing == len(self.play_list)-1

    def play_list_add(self, plist):
        self.play_list.append(plist)
        print(self.play_list)

    def play_list_remove(self, index):
        self.play_list.remove(index)

    def play_list_clear(self):
        self.play_list = []
        self.current_playing = 0

    def get_current_play_list_item(self):
        return self.play_list[self.current_playing]

    def get_current_play_list_index(self):
        return self.current_playing

    def play_list_is_empty(self):
        return self.play_list == []

    def forward(self, jump_distance):
        time = self.get_current_time() + jump_distance
        try:
            if self.duration > time:
                print('[+] Jump to {0} seconds'.format(time))
                self.seek(time)
                self.songtime = time 
            else:
                print('[+]Jump to the end!')
                self.player.seek(self.duration() - 2)
        except AttributeError:
            pass
    
    def rewind(self, jump_distance):
        time = self.get_current_time() - jump_distance
        try:
            print('[+] Jump to {0} seconds'.format(time))
            self.seek(time)
            self.songtime = time
        except:
            self.player.seek(0)




"""
if __name__ == "__main__":

    window = pyglet.window.Window()
    image = pyglet.resource.image('1.jpg')

    label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
    
    @window.event
    def on_draw():
        window.clear()
        image.blit(0,0)
        label.draw()
    
    audio = AudioPlayer()
    audio.play_list_add('source/11+Someone+Like+You.wav')
   
    
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.RIGHT:
            print('The right key was pressed.')
            audio.forward(3)
        elif symbol == key.LEFT:
            print('The left arrow key was pressed.')
            audio.rewind(3)
        elif symbol == key.ENTER:
            if audio.paused_flag % 2 == 0:
                audio.pause()
            else:
                print('[+]play continue')
                audio.play()
                print(audio.get_duration())
            audio.paused_flag += 1

    # time_thread(audio, 0).start()
       
    pyglet.app.run()
"""