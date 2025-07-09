import pygame
import fluidsynth
import mido
import threading
import time

class AudioManager:
    def __init__(self):
        pygame.init()
        self.fs = fluidsynth.Synth()
        self.fs.start()
        self.sfid = self.fs.sfload("car/sounds/GeneralUser_GS_v1.471.sf2")
        self.music_channel = 0
        self.sfx_channel = 9
        self.music_thread = None
        self.stop_music_flag = threading.Event()

    def play_music(self, path):
        if self.music_thread and self.music_thread.is_alive():
            self.stop_music()

        self.stop_music_flag.clear()
        self.music_thread = threading.Thread(target=self._music_player, args=(path,))
        self.music_thread.daemon = True
        self.music_thread.start()

    def _music_player(self, path):
        try:
            mid = mido.MidiFile(path)
            for msg in mid.play():
                if self.stop_music_flag.is_set():
                    break
                self.fs.router.handle_midi_event(msg)
        except Exception as e:
            # Handle exceptions, e.g., file not found
            pass

    def stop_music(self):
        if self.music_thread and self.music_thread.is_alive():
            self.stop_music_flag.set()
            self.music_thread.join()

    def play_sfx(self, note):
        self.fs.noteon(self.sfx_channel, note, 127)
        # Schedule note off to prevent stuck notes
        off_thread = threading.Thread(target=self._note_off_sfx, args=(note,))
        off_thread.daemon = True
        off_thread.start()

    def _note_off_sfx(self, note):
        time.sleep(0.5) # Duration of the sound effect
        self.fs.noteoff(self.sfx_channel, note)

    def __del__(self):
        self.fs.delete()

