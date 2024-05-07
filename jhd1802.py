#!/usr/bin/env python
import oled
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# Copyright (C) 2018  Seeed Technology Co.,Ltd.
#
# This is the library for Grove Base Hat
# which used to connect grove sensors for Raspberry Pi.
'''
This is the code for
    - `Grove - 16 x 2 LCD (Black on Red) <https://www.seeedstudio.com/Grove-16-x-2-LCD-Black-on-Re-p-3197.html>`_
    - `Grove - 16 x 2 LCD (Black on Yellow) <https://www.seeedstudio.com/Grove-16-x-2-LCD-Black-on-Yello-p-3198.html>`_
    - `Grove - 16 x 2 LCD (White on Blue) <https://www.seeedstudio.com/Grove-16-x-2-LCD-White-on-Blu-p-3196.html>`_

Examples:

    .. code-block:: python

        import time
        from grove.factory import Factory

        # LCD 16x2 Characters
        lcd = Factory.getDisplay("JHD1802")
        rows, cols = lcd.size()
        print("LCD model: {}".format(lcd.name))
        print("LCD type : {} x {}".format(cols, rows))

        lcd.setCursor(0, 0)
        lcd.write("hello world!")
        lcd.setCursor(0, cols - 1)
        lcd.write('X')
        lcd.setCursor(rows - 1, 0)
        for i in range(cols):
            lcd.write(chr(ord('A') + i))

        time.sleep(3)
        lcd.clear()
'''
import upm.pyupm_jhd1313m1 as upmjhd
from grove.display.base import *
import sys, mraa

# sphinx autoapi required
__all__ = ["JHD1802"]

class JHD1802(Display):
    '''
    Grove - 16 x 2 LCD, using chip JHD1802.
        - Grove - 16 x 2 LCD (Black on Yellow)
        - Grove - 16 x 2 LCD (Black on Red)
        - Grove - 16 x 2 LCD (White on Blue)

    Also, it's our class name,
    which could drive the above three LCDs.

    Args:
        address(int): I2C device address, default to 0x3E.
    '''
    def __init__(self, address = 0x3E):
        self._bus = mraa.I2c(0)
        self._addr = address
        self._bus.address(self._addr)
        if self._bus.writeByte(0):
            print("Check if the LCD {} inserted, then try again"
                    .format(self.name))
            sys.exit(1)
        self.jhd = upmjhd.Jhd1313m1(0, address, address)

    @property
    def name(self):
        '''
        Get device name

        Returns:
            string: JHD1802
        '''
        return "JHD1802"

    def type(self):
        '''
        Get device type

        Returns:
            int: ``TYPE_CHAR``
        '''
        return TYPE_CHAR

    def size(self):
        '''
        Get display size

        Returns:
            (Rows, Columns): the display size, in characters.
        '''
        # Charactor 16x2
        # return (Rows, Columns)
        return 2, 16

    def clear(self):
        '''
        Clears the screen and positions the cursor in the upper-left corner.
        '''
        self.jhd.clear()

    def draw(self, data, bytes):
        '''
        Not implement for char type display device.
        '''
        return False

    def home(self):
        '''
        Positions the cursor in the upper-left of the LCD.
        That is, use that location in outputting subsequent text to the display.
        '''
        self.jhd.home()

    def setCursor(self, row, column):
        '''
        Position the LCD cursor; that is, set the location
        at which subsequent text written to the LCD will be displayed.

        Args:
            row   (int): the row at which to position cursor, with 0 being the first row
            column(int): the column at which to position cursor, with 0 being the first column

	Returns:
	    None
        '''
        self.jhd.setCursor(row, column)

    def write(self, msg):
        '''
        Write character(s) to the LCD.

        Args:
            msg (string): the character(s) to write to the display

        Returns:
            None
        '''
        self.jhd.write(msg)

    def _cursor_on(self, enable):
        if enable:
            self.jhd.cursorOn()
        else:
            self.jhd.cursorOff()

def main():
    import time
    lcd = JHD1802()
    rows, cols = lcd.size()
    print("LCD model: {}".format(lcd.name))
    print("LCD type : {} x {}".format(cols, rows))
 
    lcd.backlight(False)
    time.sleep(1)
    lcd.backlight(True)
    lcd.setCursor(0, 0)
    lcd.write("hello world!")
    lcd.setCursor(0, cols - 1)
    lcd.write('X')
    lcd.setCursor(rows - 1, 0)
    for i in range(cols):
        lcd.write(chr(ord('A') + i))
 
    time.sleep(3)
    lcd.clear()

    Oled = oled.SH1107G_SSD1327()
    rows, cols = Oled.size()
    print("OLED model: {}".format(Oled.name))
    print("OLED type : {} x {}".format(cols, rows))

    Oled.backlight(False)
    time.sleep(1)

    Oled.backlight(True)
    Oled.setCursor(0, 0)
    Oled.write("hello world!")
    Oled.setCursor(0, cols - 1)
    Oled.write('X')
    Oled.setCursor(rows - 1, 0)
    for i in range(cols):
        Oled.write(chr(ord('A') + i))

    time.sleep(3)
    Oled.clear()

if __name__ == '__main__':
    while True:
        main()

