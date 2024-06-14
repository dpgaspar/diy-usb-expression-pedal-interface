import os
import time
import board
import analogio
import digitalio
import math
import usb_midi
import adafruit_midi
from adafruit_midi.control_change import ControlChange

controller = os.getenv("MIDI_CONTROLLER", 20)
midi_channel = os.getenv("MIDI_CHANNEL", 1)
max_raw_value = os.getenv("MAX_RAW_VALUE", 62000)
blink_on_change = os.getenv("BLINK_ON_CHANGE", 0)
step_raw_value = max_raw_value / 127

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
usb_midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=midi_channel - 1)
exp = analogio.AnalogIn(board.GP26)

old_value = 0
while True:
    new_value = exp.value
    if abs(new_value - old_value) >= step_raw_value:
        if blink_on_change:
            led.value = True
        value = int(new_value / step_raw_value)
        print(value, new_value)
        if value >= 0 and value <= 127:
            usb_midi.send(ControlChange(controller, value))
        old_value = new_value
        if blink_on_change:
            led.value = False
