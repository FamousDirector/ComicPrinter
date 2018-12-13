import RPi.GPIO as GPIO


class ComicPrinter:

    def print_comic_callback(self, channel):
        GPIO.output(5, GPIO.LOW)
        print "print comic"
        GPIO.output(5, GPIO.HIGH)

    def change_comic_callback(self, channel):
        clk_state = GPIO.input(self.clk_pin)
        if clk_state == self.clkLastState:
            dt_state = GPIO.input(self.dt_pin)
            if dt_state == clk_state:
                print "next comic"
            else:
                print "last comic"

        self.clkLastState = clk_state

    def __init__(self):

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

        # screen
        # TODO

if __name__ == '__main__':

    c = ComicPrinter()

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit

