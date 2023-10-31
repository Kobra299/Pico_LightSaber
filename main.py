import json
import os
import wave
import neopixel
import urandom
import board
import time
import machine
import asyncio
import ssd1306  # Import the SSD1306 library

# Define GPIO pins for buttons, speaker, neopixels, and OLED
button1_pin = 9
button2_pin = 34
button3_pin = 14  # Power button pin for turning the lightsaber on/off
SDA_PIN = 4
SCL_PIN = 5

# Initialize OLED display
i2c = machine.I2C(0, sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # Adjust dimensions as required

# Function to load settings from a file
def load_settings(file_path):
    with open(file_path, "r") as settings_file:
        settings = json.load(settings_file)
    return settings

# Function to load sound configurations
def load_sound_configs(directory):
    sound_configs = {}
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            config_file_path = os.path.join(root, dir_name, "config.json")
            if os.path.exists(config_file_path):
                with open(config_file_path, "r") as sound_config_file:
                    sound_configs[dir_name] = json.load(sound_config_file)
    return sound_configs

# Load settings from a file
settings = load_settings("lightsaber_settings.json")

# Load sound configurations from a folder
sounds_directory = "Sounds"
sound_configs = load_sound_configs(sounds_directory)

# Function to update the OLED display
def update_oled_display(text):
    oled.fill(0)
    oled.text(text, 0, 0)
    oled.show()

lightsaber_on = False
settings_mode = False

button1_press_start = 0
button2_press_start = 0
button3_press_start = 0

def button_pressed_for_duration(start_time, duration):
    return time.ticks_ms() - start_time >= duration

while True:
    # Check power button state
    if machine.Pin(button3_pin).value() == 0:
        if lightsaber_on:
            lightsaber_on = False
            # Implement the turn off logic
            update_oled_display("Lightsaber Off")
        else:
            lightsaber_on = True
            # Implement the turn on logic
            update_oled_display("Lightsaber On")

    # Check button 1 state
    if machine.Pin(button1_pin).value() == 0:
        button1_press_start = time.ticks_ms()

    if machine.Pin(button1_pin).value() == 1:
        button1_press_duration = time.ticks_ms() - button1_press_start

        if button1_press_duration >= 3000:
            settings_mode = True
            # Add your settings mode code here
            # Example: update_oled_display("Settings Mode")
        else:
            # Handle normal lightsaber functionality for button 1
            pass  # Add your logic here

    # Check button 2 state
    if machine.Pin(button2_pin).value() == 0:
        button2_press_start = time.ticks_ms()

    if machine.Pin(button2_pin).value() == 1:
        button2_press_duration = time.ticks_ms() - button2_press_start

        if settings_mode:
            # Inside settings mode
            # Your code to cycle through settings here
            # Example: update_oled_display("Cycling through settings")

            if button_pressed_for_duration(button2_press_start, 3000):
                # Save the selected settings
                settings_mode = False  # Exit settings mode
                # Example: update_oled_display("Settings Saved")

    await asyncio.sleep(0.1)
