import time
import traceback
from gpiozero import LED, Button
import requests.exceptions
import usb.core
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

import print_comic


class ComicPrinter:

    def print_comic_callback(self, channel):
        self.button_light.off()
        try:
            self.update_screen('Downloading comic...')
            if self.random_option:
                img = print_comic.get_comic_image(self.comic_lookup_array[self.comic_index], 'random')
            else:
                img = print_comic.get_comic_image(self.comic_lookup_array[self.comic_index])

            self.update_screen('Printing...')
            print_comic.print_comic(img)

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
            self.button_light.on()
            self.show_menu()

    def change_comic_callback(self, channel):
        clk_state = self.encoder_turn_left.is_pressed
        if clk_state == self.clkLastState:
            dt_state = self.encoder_turn_right.is_pressed
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

        self.comic_name_array = ['xkcd', 'Dilbert', 'Calvin & Hobbes', 'Overboard', 'Peanuts']
        self.comic_lookup_array = ['xkcd', 'dilbert', 'calvin', 'overboard', 'peanuts']
        self.comic_index = 0

        self.random_option = False

        self.clkLastState = False

        # encoder pins
        self.en_clk_pin = 20   # encoder left - pin 37
        self.en_dt_pin = 21   # encoder right - pin 36
        self.en_push_pin = 4  # encoder push - pin 7

        # push button pins
        self.button_push_pin = 12  # push button - pin 32
        self.button_light_pin = 5  # button LED - pin 29

        # inputs
        self.encoder_turn_left = Button(self.en_clk_pin)
        self.encoder_turn_right = Button(self.en_dt_pin)
        self.encoder_push = Button(self.en_push_pin)
        self.button_push = Button(self.button_push_pin)

        self.encoder_turn_left.when_pressed = self.change_comic_callback
        self.encoder_push.when_pressed = self.switch_data_callback
        self.button_push.when_pressed = self.print_comic_callback

        # outputs
        self.button_light = LED(self.button_light_pin)
        self.button_light.on()

        # screen
        serial = i2c(port=1, address=0x3c)
        self.screen = ssd1306(serial, rotate=0)
        self.show_menu()


if __name__ == '__main__':

    c = ComicPrinter()

    while True:
        time.sleep(100)

