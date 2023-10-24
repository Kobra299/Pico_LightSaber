import ujson
import os
import wave
import neopixel
import urandom
import board
import time
import machine
# import Adafruit_Python_CharLCD as LCD #Need to find right library

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for buttons, speaker, and neopixels
button1_pin = 9
button2_pin = 34
speaker_pin = 11
neo_pixel_pin = board.GP10

# Initialize buttons and speaker
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize speaker
pwm_speaker = PWM(Pin(speaker_pin))
pwm_speaker.duty_u16(0)

# Initialize LCD display
lcd = LCD.Adafruit_CharLCDPlate()


# Load settings from lightsaber_settings.json
with open("lightsaber_settings.json", "r") as settings_file:
    settings = ujson.load(settings_file)

# Define the path to the sounds directory
sounds_directory = "sounds"

# Function to load sound configurations from a folder
def load_sound_configs(directory):
    sound_configs = {}
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            config_file_path = os.path.join(root, dir_name, "config.json")
            if os.path.exists(config_file_path):
                with open(config_file_path, "r") as sound_config_file:
                    sound_configs[dir_name] = ujson.load(sound_config_file)
    return sound_configs

# Load sound configurations for different sound folders
sound_configs = load_sound_configs(sounds_directory)

# Initialize and configure the accelerometer
# (Make sure to add accelerometer initialization code here)

# Initialize and configure NeoPixels
num_pixels = settings["NeoPixel"]["NumPixels"]
neo_pixel_pin = board.GP10
pixels = neopixel.NeoPixel(neo_pixel_pin, num_pixels)

# Define a list of movement thresholds for different effects
movement_thresholds = {
    "Swing": 2.0,
    "Hit": 3.0,
    # Add more movement types and thresholds as needed
}

# Define the event loop
loop = asyncio.get_event_loop()

# Function to detect and respond to movements
async def detect_movements():
    while True:
        # Read accelerometer data
        # (Add accelerometer data reading code here)

        for movement, threshold in movement_thresholds.items():
            if accelerometer_data['x'] > threshold:
                # A swing movement is detected
                play_random_sound_effect(sound_effects[movement])
            elif accelerometer_data['y'] > threshold:
                # A hit movement is detected
                play_random_sound_effect(sound_effects[movement])
            # Add more movement detection logic as needed

        await asyncio.sleep(0.1)

# Create a task to detect movements asynchronously
loop.create_task(detect_movements())

# Main loop for settings management, button actions, and NeoPixel updates
while True:
    # Check button 1 state
    if machine.Pin(9).value() == 0:  # Replace with the actual GPIO pin for button 1
        # Button 1 is pressed, perform action
        button1_pressed(None)

    # Check button 2 state
    if machine.Pin(34).value() == 0:  # Replace with the actual GPIO pin for button 2
        # Button 2 is pressed, perform action
        button2_pressed(None)

    # Example: Set NeoPixels based on the "Blade Color" setting
    blade_color = settings["Settings"]["BladeColor"]
    color_mappings = settings["Colors"]
    if blade_color in color_mappings:
        set_neopixel_color([int(x) for x in color_mappings[blade_color].split(",")])

    await asyncio.sleep(0.1)  # Add a small delay to avoid rapid loop iterations

# Run the event loop
loop.run_forever()
