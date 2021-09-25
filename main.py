import time
import traceback
import RPi.GPIO as GPIO
import requests.exceptions
import usb.core
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

import print_comic


class ComicPrinter:

    def print_comic_callback(self, channel):
        GPIO.output(5, GPIO.LOW)
        self.update_screen('PRINTING...')
        try:
            if self.random_option:
                print_comic.print_comic(self.comic_lookup_array[self.comic_index], 'random')
            else:
                print_comic.print_comic(self.comic_lookup_array[self.comic_index])
        except usb.core.USBTimeoutError:
            print(traceback.format_exc())
            self.update_screen("A timeout \nerror has \noccurred")
            time.sleep(5)
        except requests.exceptions.InvalidSchema:
            print(traceback.format_exc())
            self.update_screen("Could not find \ncomic to print")
            time.sleep(5)
        except Exception:
            print(traceback.format_exc())
            self.update_screen("An unknown \nerror has \n occurred")
            time.sleep(5)
        finally:
            GPIO.output(5, GPIO.HIGH)
            self.show_menu()

    def change_comic_callback(self, channel):
        clk_state = GPIO.input(self.clk_pin)
        if clk_state == self.clkLastState:
            dt_state = GPIO.input(self.dt_pin)
            if dt_state == clk_state:
                self.increment_comic_index()
                self.show_menu()
            else:
                self.decrement_comic_index()
                self.show_menu()

        self.clkLastState = clk_state

    def switch_data_callback(self, channel):
        self.random_option = not self.random_option
        self.show_menu()

    def increment_comic_index(self):
        if self.comic_index < len(self.comic_lookup_array) - 1:
            self.comic_index += 1
        else:
            self.comic_index = 0

    def decrement_comic_index(self):
        if self.comic_index > 0:
            self.comic_index -= 1
        else:
            self.comic_index = len(self.comic_lookup_array) - 1

    def show_menu(self):
        if not self.random_option:
            display_string = ('Print today\'s: \n' + self.comic_name_array[self.comic_index]
                              + '\ncomic strip?')
        else:
            display_string = ('Print a random: \n' + self.comic_name_array[self.comic_index]
                              + '\ncomic strip?')

        self.update_screen(display_string)

    def update_screen(self, display_string):
        with canvas(self.screen) as draw:
            draw.rectangle(self.screen.bounding_box, outline="white", fill="black")
            draw.text((10, 15), display_string, fill="white")

    def __init__(self):

        self.comic_name_array = ['xkcd', 'Dilbert', 'Calvin & Hobbes', 'Cyanide & Happiness', 'Overboard']
        self.comic_lookup_array = ['xkcd', 'dilbert', 'calvin', 'cyanide', 'overboard']
        self.comic_index = 0

        self.random_option = False

        self.clkLastState = False

        self.clk_pin = 20
        self.dt_pin = 21

        # GPIO SETUP
        GPIO.setmode(GPIO.BCM)

        # inputs
        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # encoder left - pin 37
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # encoder right - pin 36
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # push button - pin 32
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # encoder push - pin 7

        GPIO.add_event_detect(self.clk_pin, GPIO.FALLING, callback=self.change_comic_callback, bouncetime=300)
        GPIO.add_event_detect(12, GPIO.FALLING, callback=self.print_comic_callback, bouncetime=300)
        GPIO.add_event_detect(4, GPIO.FALLING, callback=self.switch_data_callback, bouncetime=300)

        # outputs
        GPIO.setup(5, GPIO.OUT)  # button LED - pin 29
        GPIO.output(5, GPIO.HIGH)

        # screen
        serial = i2c(port=1, address=0x3c)
        self.screen = ssd1306(serial, rotate=0)
        self.show_menu()


if __name__ == '__main__':

    c = ComicPrinter()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit
