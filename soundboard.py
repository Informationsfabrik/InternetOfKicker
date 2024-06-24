import os
from time import sleep
import pygame
from pynput import keyboard
from pynput.keyboard import Key

from db_connection import Goal, Storage

class Soundboard:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

        self.current_sound = None

        self.sound_mapping = {
            'f': 'sounds/Freundschaftsspiel.mp3',
            'g': 'sounds/geschenktesTor.mp3',
            'v': 'sounds/Verteidigung.mp3',
            Key.up: 'sounds/Song2.mp3',
            'p': 'sounds/Pfostentor.mp3',
            'r': 'sounds/suiiiiii.mp3',
            'm': 'sounds/ankara-messi-sound-effect-made-with-Voicemod.mp3',
            Key.down: 'sounds/wah-wah-sad-trombone-6347.mp3',
            'e': 'sounds/windoof_error.mp3'
        }

        self.storage = self.setup_storage()
        self.play_initial_sound()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def setup_storage(self):
        if os.path.isfile(os.getcwd() + "/.env"):
            try:
                return Storage()
            except:
                print("WARNING: Error connecting to db. Running as soundboard only. Goals are not logged in db.")
                self.play_error_sound()
                return None
        else:

            self.play_error_sound()
            print("WARNING: .env not found. Running as soundboard only. Goals are not logged in db.")
            return None

    def play_initial_sound(self):
        self.play_sound_file('sounds/ea_sports.mp3')

    def play_error_sound(self):
        # sleep(10)
        self.play_sound_file('sounds/windoof_error.mp3')
        sleep(7) #need to sleep to avoid cancelling the sound

    def play_sound_file(self, sound_file):
        self.stop_current_sound()
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
        self.current_sound = sound

    def stop_current_sound(self):
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None

    def play_sound(self, key):
        key = key if type(key) == Key else key.char
        print(key)
        sound_file = self.sound_mapping.get(key)
        if sound_file:
            self.play_sound_file(sound_file)

        match key:
            case Key.left:
                goal = Goal("blue")
                self.play_sound_file(self.sound_mapping["r"])
            case Key.right:
                goal = Goal("red")
                self.play_sound_file(self.sound_mapping["m"])
            case _:
                return

        if self.storage:
            self.storage.save_goal(goal)

    def on_press(self, key):
        self.play_sound(key)

    def run(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.play_error_sound()
            self.play_error_sound()
            self.play_error_sound()
            raise e
        finally:
            self.listener.stop()
            pygame.quit()

if __name__ == "__main__":
    soundboard = Soundboard()
    soundboard.run()
