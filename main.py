import adafruit_dotstar  # Our LED library
import digitalio
import board
import math
import time

print("LumiDrive v10")

# Setting up the product's blue stat LED to blink
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# These two variables should be adjusted to reflect the number of LEDs you have
# and how bright you want them.
num_pixels = 40
brightness = 0.2

# This creates the instance of the DoTStar library.
pixels = adafruit_dotstar.DotStar(
    board.SCK, board.MOSI, num_pixels, brightness=brightness, auto_write=False
)

# Some standard colors.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)


# Animation setup
max_tick = 9999
LR_FIREPLACE = 16
LR_TO_KITCHEN = [17, 18, 19, 20, 21, 22]
KITCHEN_TO_DEN = [22, 23, 24, 25, 26]
BED1_TO_LR = [10, 11, 12, 13, 14, 15, 16, 17]

# This function takes a color and a dely and fills the entire strand with that color.
# The delay is given in the case you use multiple color fills in a row.


def color_fill(color, wait):
    pixels.fill(color)
    pixels.show()
    time.sleep(wait)


print("Clearing LEDs.")
color_fill(BLACK, 0)

tick = 0


def flicker(pos, colors):
    if tick % 2 < 1:
        pixels[pos] = colors[0]
    else:
        pixels[pos] = colors[1]


def blink_board_light():
    led.value = tick % 20 < 5


def fireplace(start=0, end=max_tick):
    if tick == start:
        print("fireplace", start, end)
    if start <= tick < end:
        flickering = tick < end - 1
        pos = LR_FIREPLACE
        if flickering:
            flicker(pos, [(255, 0, 0, 0.1), (255, 150, 0, 0.1)])
        else:
            pixels[pos] = BLACK


def walk(start, path, reverse=False):
    if tick == start:
        print("walk", start, path, reverse)
    if start <= tick < start+len(path):
        pos = tick % start
        old_pos = pos - 1
        if reverse:
            pos = (len(path) - pos) - 1
            old_pos = pos + 1
        # print(pos, old_pos, len(path))
        pixels[path[pos]] = WHITE
        if 0 <= old_pos < len(path):
            pixels[path[old_pos]] = BLACK


while True:
    # print(tick)
    blink_board_light()

    # stand_by_fireplace(True)
    walk(10, BED1_TO_LR)
    fireplace(30, 250)
    walk(130, LR_TO_KITCHEN)
    walk(160, KITCHEN_TO_DEN)
    walk(180, KITCHEN_TO_DEN, reverse=True)
    walk(190, LR_TO_KITCHEN, reverse=True)
    walk(240, BED1_TO_LR, reverse=True)
    if tick > 300:
        tick = 0

    pixels.show()
    time.sleep(0.01)
    tick = tick + 1

    # travel_single(WHITE, 0.01)
    # led.value = True
    # time.sleep(0.5)
    # led.value = False
    # time.sleep(0.5)
