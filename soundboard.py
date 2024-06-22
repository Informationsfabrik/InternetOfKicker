import os
from time import sleep
import pygame
from pynput import keyboard
from pynput.keyboard import Key

from db_connection import Goal, Storage

# Initialize Pygame
pygame.init()

pygame.mixer.Sound('sounds/ea_sports.mp3').play()
# Define a dictionary to map keys to sounds
sound_mapping = {
    'f': 'sounds/Freundschaftsspiel.mp3',
    'g': 'sounds/geschenktesTor.mp3',
    'v': 'sounds/Verteidigung.mp3',
    Key.up:'sounds/Song2.mp3',
    'p': 'sounds/Pfostentor.mp3',
    'r': 'sounds/suiiiiii.mp3',
    'm': 'sounds/ankara-messi-sound-effect-made-with-Voicemod.mp3',
    Key.down: 'sounds/wah-wah-sad-trombone-6347.mp3',
    'e': 'sounds/windoof_error.mp3'
}

if os.path.isfile(os.getcwd()+"/.env"):
    try:
        storage = Storage()
    except:
        pygame.mixer.Sound('sounds/windoof_error.mp3').play()
        pygame.mixer.Sound('sounds/windoof_error.mp3').play()
        storage = None
        print("WARNING: Error connecting to db. Running as soundboard only. Goals are not logged in db.")

else:
    pygame.mixer.Sound('sounds/windoof_error.mp3').play()
    print("WARNING: .env not found. Running as soundboard only. Goals are not logged in db.")
    storage = None


# Function to play a sound based on the key press
def play_sound(key):
    # Handle differences between characters and other keys
    key = key if type(key) == Key else key.char
    print(key)
    sound_file = sound_mapping.get(key)
    if sound_file:
        # Load and play the sound
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    # Handle special keys (e.g., shift, ctrl) by ignoring them
    match key:
        case Key.left:
            goal = Goal("blue")
            pygame.mixer.Sound(sound_mapping["r"]).play()
        case Key.right:
            goal = Goal("red")
            pygame.mixer.Sound(sound_mapping["m"]).play()
        case _:
            return
    if storage:
        storage.save_goal(goal)


# Listener for keyboard key press events
def on_press(key):
    # print(key.char)
    play_sound(key)

# Create a keyboard listener
listener = keyboard.Listener(on_press=on_press)

# Start the listener
listener.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
except Exception as e:
    pygame.mixer.Sound('sounds/windoof_error.mp3').play()
    sleep(0.1)
    pygame.mixer.Sound('sounds/windoof_error.mp3').play()  
    sleep(0.1)
    pygame.mixer.Sound('sounds/windoof_error.mp3').play()  
    sleep(3)
    raise e
finally:
    listener.stop()
    pygame.quit()
