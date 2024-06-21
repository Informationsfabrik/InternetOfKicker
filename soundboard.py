import os,sys
import pygame
from pynput import keyboard
from pynput.keyboard import Key

from db_connection import Goal, Storage

# Initialize Pygame
pygame.init()

pygame.mixer.Sound('sounds/ea_sports.mp3').play()
# Define a dictionary to map keys to sounds
sound_mapping = {
    'w': 'sounds/Freundschaftsspiel.mp3',
    'a': 'sounds/geschenktesTor.mp3',
    's': 'sounds/Verteidigung.mp3',
    'd': 'sounds/Pfostentor.mp3',
    'r': 'sounds/suiiiiii.mp3',
    'm': 'sounds/ankara-messi-sound-effect-made-with-Voicemod.mp3',
    't': 'sounds/wah-wah-sad-trombone-6347.mp3',
    'e': 'sounds/windoof_error.mp3'
}

if os.path.isfile(os.getcwd()+"/.env"):
    storage = Storage()
else:
    print("WARNING: .env not found. Running as soundboard only. Goals are not logged in dbeeeer.")
    storage = None


# Function to play a sound based on the key press
def play_sound(key):
    try:
        # Convert the key to a character and find the corresponding sound
        k = key.char
        print(k)
        sound_file = sound_mapping.get(k)
        if sound_file:
            # Load and play the sound
            sound = pygame.mixer.Sound(sound_file)
            sound.play()
    except AttributeError:
        # Handle special keys (e.g., shift, ctrl) by ignoring them
        match key:
            case Key.left:
                goal = Goal("blue")
            case Key.right:
                goal = Goal("red")
            case _:
                return
        if storage:
            storage.save_goal(goal)
        pygame.mixer.Sound(sound_mapping["a"]).play()


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
finally:
    listener.stop()
    pygame.quit()
