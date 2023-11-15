import time
import board
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# MIDI setup as MIDI out device
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Define the pin numbers and corresponding MIDI notes in a dictionary
pin_to_midi = {
    board.GP7: 60, board. GP8:61, board. GP9: 62,board.GP10: 63,
    board.GP11:64, board.GP12:65, board.GP13: 66,board.GP14: 67,
    board.GP16:68, board.GP17:69, board.GP18: 70,board.GP19: 71,
    board.GP20:72, board.GP21:73, board.GP22: 74,board.GP26: 75,
}

# Create DigitalInOut objects for each button
buttons = {pin: digitalio.DigitalInOut(pin) for pin in pin_to_midi.keys()}
for button in buttons.values():
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# Note velocity
velocity = 120

# Note states
note_states = {pin: False for pin in pin_to_midi.keys()}

while True:
    # MIDI input for each button
    for pin, button in buttons.items():
        midi_note = pin_to_midi[pin]

        if not button.value and not note_states[pin]:
            midi.send(NoteOn(midi_note, velocity))
            note_states[pin] = True
        elif button.value and note_states[pin]:
            midi.send(NoteOff(midi_note, velocity))
            note_states[pin] = False

    # Add a small delay to avoid continuous MIDI messages
    time.sleep(0.01)
