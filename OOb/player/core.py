
from abc import ABCMeta, abstractmethod
import pyglet

from pyglet import media

class playCore(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.player = None
        self.media = None

    @abstractmethod
    def play(self):
        raise NotImplementedError()

    @abstractmethod
    def play_next(self):
        raise NotImplementedError()

    @abstractmethod
    def play_previous(self):
        raise NotImplementedError()

    @abstractmethod
    def load(self, uri):
        raise NotImplementedError()

    @abstractmethod
    def pause(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()

    @abstractmethod
    def seek(self, position):
        raise NotImplementedError()

    @abstractmethod
    def set_volume(self, value):
        raise NotImplementedError()

    @abstractmethod
    def get_volume(self):
        raise NotImplementedError()

    @abstractmethod
    def get_current_time(self):
        raise NotImplementedError()

    @abstractmethod
    def get_duration(self):
        raise NotImplementedError()

    @abstractmethod
    def is_media_loaded(self):
        raise NotImplementedError()

    @abstractmethod
    def is_playing(self):
        raise NotImplementedError()

    @abstractmethod
    def play_list_add(self, plist):
        raise NotImplementedError()

    @abstractmethod
    def play_list_remove(self, index):
        raise NotImplementedError()

    @abstractmethod
    def play_list_clear(self):
        raise NotImplementedError()

    @abstractmethod
    def get_current_play_list_item(self):
        raise NotImplementedError()

    @abstractmethod
    def get_current_play_list_index(self):
        raise NotImplementedError()

    @abstractmethod
    def play_list_is_empty(self):
        raise NotImplementedError()