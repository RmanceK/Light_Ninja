"""
Adaptation from :
MicroPython P9813 RGB LED driver
https://github.com/mcauser/micropython-p9813

MIT License
Copyright (c) 2017 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from grove.gpio import GPIO

class GroveChainableLED:
    def __init__(self, pin_clk, pin_data, num_leds):
        self.pin_clk = GPIO(pin_clk, GPIO.OUT)
        self.pin_data = GPIO(pin_data, GPIO.OUT)
        self.num_leds = num_leds
        self.reset()

    def __setitem__(self, index, val):
        offset = index * 3
        for i in range(3):
            self.buf[offset + i] = val[i]

    def __getitem__(self, index):
        offset = index * 3
        return tuple(self.buf[offset + i] for i in range(3))

    def fill(self, color):
        for i in range(self.num_leds):
            self[i] = color

    def reset(self):
        self.buf = bytearray(self.num_leds * 3)
        # Begin data frame 4 bytes
        self._frame()
        # 4 bytes for each led (checksum, blue, green, red)
        for i in range(self.num_leds):
            self._write_byte(0xC0)
            for i in range(3):
                self._write_byte(0)
        # End data frame 4 bytes
        self._frame()

    def write(self):
        # Begin data frame 4 bytes
        self._frame()

        # 4 bytes for each led (checksum, blue, green, red)
        for i in range(self.num_leds):
            self._write_color(self.buf[i * 3], self.buf[i * 3 + 1], self.buf[i * 3 + 2])

        # End data frame 4 bytes
        self._frame()

    def _frame(self):
        # Send 32x zeros
        self.pin_data.write(0)
        for i in range(32):
            self._clk()

    def _clk(self):
        self.pin_clk.write(0)
        #sleep(0.01) # works without it
        self.pin_clk.write(1)
        #sleep(0.01) # works without it

    def _write_byte(self, b):
        if b == 0:
            # Fast send 8x zeros
            self.pin_data.write(0)
            for i in range(8):
                self._clk()
        else:
            # Send each bit, MSB first
            for i in range(8):
                if ((b & 0x80) != 0):
                    self.pin_data.write(1)
                else:
                    self.pin_data.write(0)
                self._clk()

                # On to the next bit
                b <<= 1

    def _write_color(self, r, g, b):
        # Send a checksum byte with the format "1 1 ~B7 ~B6 ~G7 ~G6 ~R7 ~R6"
        # The checksum colour bits should bitwise NOT the data colour bits
        checksum = 0xC0 # 0b11000000
        checksum |= (b >> 6 & 3) << 4
        checksum |= (g >> 6 & 3) << 2
        checksum |= (r >> 6 & 3)

        self._write_byte(checksum)

        # Send the 3 colours
        self._write_byte(b)
        self._write_byte(g)
        self._write_byte(r)


# Début du programme
# Importation de la classe qui permet d'allumer les lumières.
chain = GroveChainableLED(5,6,4)

# Étains les lumières au début du programme.
chain[0] = (0, 0, 0)
chain[1] = (0, 0, 0)
chain[2] = (0, 0, 0)
chain[3] = (0, 0, 0)
chain.write()

# Définition des couleurs utilisées dans la suite du programme.
Rouge = (255, 0, 0)
Vert = (0, 255, 0)
Bleu = (0, 0, 255)
Blanc = (255, 192, 203)
Rose = (165, 42, 42)
Or = (255, 215, 0)
Violet = (128, 0, 128)

from threading import Lock
led_lock = Lock()

def allumer(num_led : int,couleur : list):
    # Allume les lumières individuellement d'une couleur choisie.
    with led_lock:
        chain[num_led] = couleur
        chain.write()

def eteindre(num_led : int):
    # Etain les lumières individuellement.
    with led_lock:
        chain[num_led] = (0,0,0)
        chain.write()

def tout_eteindre():
    # Etain toutes les lumières.
    with led_lock:
        for i in range(chain.num_leds):
            chain[i] = (0,0,0)
    chain.write()
