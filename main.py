import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import print_comic


class ComicPrinter:

    def print_comic_callback(self, channel):
        GPIO.output(5, GPIO.LOW)
        self.update_screen(input='PRINTING...')
        print_comic.print_comic(self.comic_lookup_array[self.comic_index])
        GPIO.output(5, GPIO.HIGH)
        self.update_screen()

    def change_comic_callback(self, channel):
        clk_state = GPIO.input(self.clk_pin)
        if clk_state == self.clkLastState:
            dt_state = GPIO.input(self.dt_pin)
            if dt_state == clk_state:
                self.increment_comic_index()
                self.update_screen()
            else:
                self.decrement_comic_index()
                self.update_screen()

        self.clkLastState = clk_state


    def increment_comic_index(self):
        if self.comic_index < len(self.comic_lookup_array)-1:
            self.comic_index += 1
        else:
            self.comic_index = 0

    def decrement_comic_index(self):
        if self.comic_index > 0:
            self.comic_index -= 1
        else:
            self.comic_index = len(self.comic_lookup_array)-1

    def update_screen(self, input=None):
        if input is None:
            display_string = 'Select a comic: \n' + self.comic_name_array[self.comic_index]
        else:
            display_string = input

        with canvas(self.screen) as draw:
            draw.rectangle(self.screen.bounding_box, outline="white", fill="black")
            draw.text((5, 5), display_string, fill="white")


    def __init__(self):

        self.comic_name_array = ['xkcd', 'Dilbert', 'Calvin & Hobbes', 'Cyanide & Happiness', 'Overboard']
        self.comic_lookup_array = ['xkcd', 'dilbert', 'calvin', 'cyanide', 'overboard']
        self.comic_index = 0

        self.clkLastState = False

        self.clk_pin = 16
        self.dt_pin = 12

        # GPIO SETUP
        GPIO.setmode(GPIO.BCM)

        # inputs
        GPIO.setup(self.clk_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # encoder left - pin 37
        GPIO.setup(self.dt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # encoder right - pin 36
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # push button - pin 32

        GPIO.add_event_detect(self.clk_pin, GPIO.FALLING, callback=self.change_comic_callback, bouncetime=50)
        GPIO.add_event_detect(26, GPIO.FALLING, callback=self.print_comic_callback, bouncetime=300)

        # outputs
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(5, GPIO.HIGH)

        # screen
        serial = i2c(port=1, address=0x3c)
        self.screen = ssd1306(serial, rotate=0)
        self.update_screen()

if __name__ == '__main__':

    c = ComicPrinter()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit

