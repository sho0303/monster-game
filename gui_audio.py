"""
Audio handler for the game GUI
"""
from pygame import mixer


class Audio:
    """Audio handler"""
    @staticmethod
    def play_sound(name):
        try:
            mixer.init()
            mixer.music.load(f'./sounds/{name}')
            mixer.music.play()
        except:
            pass
