# MusicBox
Music Box powered by RPi Pico made for my lovely friend Erin. Swaps between her 2 wedding songs to be played upon opening the lid, with a secret hidden mickey button that when pressed while the box is opening will play Merida's theme.

## Wooden Music Box
Handmade by loml Bobby

## Hardware
[Raspberry Pi Pico H](https://www.adafruit.com/product/5525)

[Adafruit I2S 3W Class D Amplifier Breakout - MAX98357A](https://www.adafruit.com/product/3006)

[MicroSD card breakout board+](https://www.adafruit.com/product/254)

[Mini Oval Speaker - 8 Ohm 1 Watt](https://www.adafruit.com/product/3923)

Resistors and Push Button from my circuits lab caboodle from college I never got rid of

## Software
CircuitPython libraries provided by AdaFruit

Thonny IDE

## Music 
Wishes and Happily Ever After

Used AnthemScore convert MP3 to Midi files, cleaned up by hand to generate the sheet music played by the pianist at the wedding :')

Used midi file to create a music box version of each song, cut the Merida theme out of HAE

## Tracking Future Improvements

Python in general has limitations with handling true simultaneous threading. My intent was to be able to press the button while the box was open to begin playing Merida's song, but there was noticeable interference in the main song's audio while python was swapping between the main thread and the button ISR. Future improvement would be implementing in C to use button as initially intended, or using 2 python applications that run in parallel rather than having 1 app that tries to run 2 threads. Not sure how CircuitPython would be able to handle 2 parallel applications trying to access the same pieces of hardware.

Still not loving available options to power the Pi. Original plan was to use AA batteries but I have sustainability and longevity concerns. Most sustainable and reliable power source is the USB C port on the Pi, which means the Music Box needs to be delivered with appropriate power block and long enough USB cable. I'm not loving this option either as it means the box will have to be placed somewhere in proximity to an outlet. I have some possibly unreasonable concerns with the USB C power source causing boot issues with the Pi that would bypass running the app on power on. 
