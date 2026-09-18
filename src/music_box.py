'''
This is a music box made for Erin Nash Berg to celebrate her wedding by playing
the songs she and her bridesmaids walked down the aisle to. The songs were
arranged by Katie Hobble.

Upon opening the music box, one of two songs will play, cycling each time the
lid opens. When the secret button is pressed while opening the box, a secret
song plays instead!

Items used:
Raspberry Pi Pico RP2040
Adafruit 5V Ready Micro-SD Breakout Board+ + 8Gb Micro-SD card
Adafruit MAX98357 i2S Amp
Mini Oval Speaker - 8 Ohm 1 Watt
Magnetic contact switch (door sensor)
'''

import board

import sdcardio
import busio   
import storage

import audiocore
import audiobusio

import json
from digitalio import DigitalInOut, Direction, Pull

from collections import OrderedDict

global btn
btn = DigitalInOut(board.GP0)

global prev_state
prev_state=btn.value

global btn_pressed
btn_pressed=False

global playlist
playlist = OrderedDict()

global memory
memory = OrderedDict()


##########
##########

#
# function: initialize
#
def initialize():
    
    #
    # Set up the button pin and attach ISR to falling edge of the button pin
    #
    print ("initializing")
    btn.direction = Direction.INPUT
    btn.pull=Pull.UP
    
    #
    # When button is pressed, btn.value will be FALSE
    #
    global btn_pressed
    btn_pressed=not btn.value
    
    #
    # Define the CS (Chip Select) pin for your SD card breakout board.
    #
    cs_pin = board.GP13
    spi_sck = board.GP10
    spi_tx = board.GP11
    spi_rx = board.GP12
    
    #
    # Initialize the SD card
    #
    spi=busio.SPI(spi_sck, MOSI=spi_tx, MISO=spi_rx)
    sd = sdcardio.SDCard(spi, cs_pin)

    #
    # Mount the SD card filesystem
    #
    vfs = storage.VfsFat(sd)
    storage.mount(vfs, "/sd")
    
    #
    # Define the I2S pins for your setup
    #
    bclk = board.GP18
    lrclk = board.GP19
    data = board.GP21
    
    #
    # Initialize the I2S audio output
    #
    global audio
    audio=audiobusio.I2SOut(bit_clock=bclk, word_select=lrclk, data=data)
    
    
    #
    # Dictionary with songs in order
    # key = action performed
    #       first_play = box was opened and first song should be played
    #       second_play = box was opened and seccond song should be played
    #       button = SECRET BUTTON SONG
    # value = song to play
    #
    global playlist
    playlist["first_play"]  = "wishes.wav"
    playlist["second_play"] = "hae.wav"
    playlist["button"]      = "merida.wav"


##########
##########

#
# function: remember
#
# Read the brain and write a new future
#
# returns: action to be performed based on what's happened in the past
#          (~if there is one~)
#
def remember():
    
    #
    # If the button was pressed upon start, then play the secret song instead
    #
    global btn_pressed
    if btn_pressed == True:
        action="button"
    else:   
        #
        # Establish baseline memories
        #
        action = "first_play"
        count  = 0
       
        #
        # Peek inside the brain to see the past
        #
        f=open("/brain.txt", "r")
            
        #
        # Read the  b r a i n  and reclaim any memories
        #
        brain = f.read()
        global memory
        try:
            memory = json.loads(brain)
            action = memory["action"]
            count  = memory["count"]
        except:
            print ("First timer")
        
        f.close()
        
                
        #
        # Create a new memory for the future, but remember to keep secrets!!
        #
        global playlist
        next_count = count+1
        if next_count >= len(playlist)-1:
            next_count = 0
            
        #
        # Prophesize the next action in the  b r a i n
        #
        all_actions = list(playlist.keys())
        print("next_count: ", next_count)
        next_action = all_actions[next_count]
        
        #
        # Set prophecy into stone
        #
        store_thoughts(next_action, next_count)
    
    #
    # Now sing for me paolo
    #       
    return action
        

##########
##########
    
#
# function: store_thoughts
# input: action - the action to be remembered
#        count  - counter for prophesizing
#
def store_thoughts(action, count):
    
    #
    # Peek inside the brain to set the future 
    #
    with open("/brain.txt", "w+") as f:
        
        #
        # Store this moment for future us <3
        #
        memory["action"] = action
        memory["count"] = count
        the_future = json.dumps(memory)        
        f.write(the_future)
    
##########
##########

#
# function: play_song
# input: action - decides what song to play from SD card
#
def play_song(action):

    #
    # Open the WAV file and play it
    #
    cur_song = playlist[action]
    with open("/sd/" + cur_song, "rb") as f:
        wav = audiocore.WaveFile(f)
        audio.play(wav)
        print ("playing " + cur_song)
        while audio.playing:
            pass    
    
##########
##########

#
# function: main
#
def main():

    #
    # Determine what we're playing by identifying the current action
    #
    action = remember()
            
    #
    # Play the song!!
    #
    while True:
        play_song(action)
            
##########
##########
    
initialize()
main()

