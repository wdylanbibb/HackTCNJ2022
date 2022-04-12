import threading
from playsound import playsound

def play_sound(name: str):
    playsound(f'sfx/{name}.wav', block=True)
