from threading import Thread, main_thread
import time
from playsound import playsound
from pydub import AudioSegment
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.mixer as mixer

sound_started = -1
sound_len = -1

def play_sound(name: str, *, wait = True):
    global sound_started, sound_len
    if wait and sound_len + sound_started > 0 and sound_len + sound_started > time.time() * 1000: return
    sound_len = len(AudioSegment.from_wav(f'sfx/{name}.wav'))
    playsound(f'sfx/{name}.wav', block=False)
    sound_started = round(time.time() * 1000)

song_queue: list[dict] = []
loop_queue = True
currIndex = 0
currThread = None

def init_music():
    mixer.init()
    pygame.init()
    clear_queue()

def add_song_to_queue(name: str, loop = False):
    song_queue.append({'song': f'music/{name}.wav', 'loop': loop})

def set_loop_queue(loop: bool):
    global loop_queue
    loop_queue = loop

def set_music_vol(vol: float):
    mixer.music.set_volume(vol)

def clear_queue():
    global currIndex
    song_queue.clear()
    stop_music()
    currIndex = 0

def next_song():
    global currIndex
    stop_music()
    if loop_queue:
        currIndex = (currIndex + 1) % len(song_queue)
    else:
        currIndex += 1
        if currIndex > len(song_queue) - 1:
            currIndex = -1
    play_next()

def unpause_music():
    if not mixer.music.get_busy():
        mixer.music.unpause()

def song_finished():
    global currIndex
    if len(song_queue) == 0: return
    if not song_queue[currIndex]['loop']:
        if loop_queue:
            currIndex = (currIndex + 1) % len(song_queue)
        else:
            currIndex += 1
            if currIndex > len(song_queue) - 1:
                currIndex = -1
    play_next()
    

def play_next():
    global currIndex, currThread
    if mixer.music.get_busy(): return
    if currIndex == -1:
        print('No music in queue!')
        currThread = None
        return
    mixer.music.load(song_queue[currIndex]['song'])
    mixer.music.play()
    mixer.music.set_endevent(100)
    def check_event():
        t = currThread
        while currThread == t:
            if not main_thread().is_alive(): return
            for ev in pygame.event.get():
                if ev.type == 100:
                    song_finished()
    currThread = Thread(target=check_event, daemon=True)
    try:
        currThread.start()
    except:
        return

def pause_music():
    if mixer.music.get_busy():
        mixer.music.pause()

def stop_music():
    mixer.music.stop()
    mixer.music.unload()
    pass