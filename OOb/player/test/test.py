#!/usr/bin/python3

import sys
import pyglet

from pyglet import media
from pyglet.window import Window

win = Window()

player = media.Player();
pyglet.resource.path = ['/home/kobe']
pyglet.resource.reindex()
src = pyglet.resource.media('facebook.mp4')
player.queue(src)

@win.event
def on_draw():
	player.get_texture().blit(0, 0, width=800, height=600)

player.play()

pyglet.app.run()