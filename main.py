import adafruit_dotstar  # Our LED library
import digitalio
import board
# import math
import time

print("LumiDrive v10")

# Setting up the product's blue stat LED to blink
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Setting up the board's onboard button
button6 = digitalio.DigitalInOut(board.D6)
button6.direction = digitalio.Direction.INPUT
button6.pull = digitalio.Pull.UP

# These two variables should be adjusted to reflect the number of LEDs you have
# and how bright you want them.
num_pixels = 44
brightness = 0.8

tick_move_dur = 0.02
tick_flicker_dur = 0.01

# This creates the instance of the DoTStar library.
pixels = adafruit_dotstar.DotStar(
    board.SCK, board.MOSI, num_pixels, brightness=brightness, auto_write=False
)

# Some standard colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# CYAN = (0, 255, 255)
# BLUE = (0, 0, 255)
# PURPLE = (180, 0, 255)
# MAGENTA = (255, 0, 20)

maria = (255, 153, 245)
jeff = (106, 157, 255)
penny = (186, 163, 119)
ruby = (234, 112, 112)
jack = (98, 193, 188)

# Animation setup
max_tick = 9999
fire = 8
tv = [29, 34]
tv_colors = [(129, 233, 226, 0.1), (240, 243, 90, 0.1)]
# starting in bedroom 1
br1_2_to_br1_1 = [1, 0]
br1_1_to_c2 = [0, 3, 2, 13]
br1_1_to_bath = [0, 3, 4, 11, 16, 15, 14]
br1_1_to_lr1 = [0, 3, 4, 5, 6]
br1_4_to_bath = [2, 3, 4, 11, 16, 15, 14]
br1_4_to_lr2 = [2, 3, 4, 5, 10, 9]
br1_1_to_k1 = [0, 3, 4, 5, 10, 18, 21, 30, 33, 39, 40, 41]
br1_4_to_k1 = [2, 3, 4, 11, 16, 23, 28, 35, 38, 39, 40, 41]
br1_4_to_dr2 = [2, 3, 4, 5, 10, 18, 21, 30]
b1_4_to_door2 = [2, 3, 4, 11, 16, 23, 28, 35, 38]

# starting in kitchen
k1_loop = [40, 41, 42, 41]
# k1_dr_loop = [40, 41, 42, 41, 40, 39, 33, 32, 33, 39]
lr2_to_k4 = [9, 18, 21, 30, 33, 39, 40, 41]
k4_to_d1 = [41, 40, 39, 38, 35, 28]
k4_to_d4 = [41, 40, 39, 33]
k4_to_laundry = [41, 40, 39, 38, 43]
k4_to_door2 = [41, 40, 39, 38]
k4_to_d2 = [41, 40, 39, 38, 35]

# starting in dining room
dr2_to_dr4 = [30, 33]
dr4_to_door2 = [33, 39, 38]

# starting in den
d2_to_bath = [35, 28, 23, 15, 14]

# starting in LR
lr1_to_b2_3 = [6, 5, 4, 11, 16, 24, 27, 36]

# This function takes a color and a dely and fills the entire strand with that color.
# The delay is given in the case you use multiple color fills in a row.


def color_fill(color, wait):
    pixels.fill(color)
    pixels.show()
    time.sleep(wait)


def travel_single(color, wait):
    num_pixels = len(pixels)
    for pos in range(num_pixels):
        pixels[pos] = color
        pixels[pos - 1] = BLACK
        pixels.show()
        time.sleep(wait)


def flicker(pos, colors):
    if tick_flicker % 2 < 1:
        pixels[pos] = colors[0]
    else:
        pixels[pos] = colors[1]


def blink_board_light():
    led.value = tick_flicker % 20 < 5


def fireplace(start=0, end=max_tick):
    if tick_move == start and tick_flicker == 0:
        print("fireplace", start, end)
    if start <= tick_move < end:
        flickering = tick_move < end - 1
        pos = fire
        if flickering:
            flicker(pos, [(246, 195, 64, 0.4), (214, 134, 14, 0.4)])
        else:
            pixels[pos] = BLACK


def tv_on(start=0, end=max_tick):
    if tick_move == start and tick_flicker == 0:
        print("tv", start, end)
    if start <= tick_move < end:
        flickering = tick_move < end - 1
        if flickering:
            flicker(tv[0], tv_colors)
            flicker(tv[1], list(reversed(tv_colors)))
        else:
            pixels[tv[0]] = BLACK
            pixels[tv[1]] = BLACK


def rest(start, color, path, reverse=False):
    if tick_move == start:
        print("rest", color, start, path, reverse)
        pos = tick_move - start
        if reverse:
            pos = (len(path) - pos) - 1
        # print(pos, old_pos, len(path))
        pixels[path[pos]] = color


def walk(start, color, path, reverse=False):
    if tick_move == start:
        print("walk", color, start, path, reverse)
    if start <= tick_move < start + len(path):
        pos = tick_move - start
        old_pos = pos - 1
        if reverse:
            pos = (len(path) - pos) - 1
            old_pos = pos + 1
        # print(pos, old_pos, len(path))
        pixels[path[pos]] = color
        if 0 <= old_pos < len(path):
            pixels[path[old_pos]] = BLACK


def loop(start, times, color, path):
    factor = 4
    if tick_move == start:
        print("loop", color, times, path)
    if start <= tick_move < (start + factor * times * len(path)):
        offset = int((tick_move - start) / factor)
        pos = offset % len(path)
        old_pos = pos - 1
        if old_pos == -1:
            old_pos = len(path)-1
        # print(offset, pos, old_pos, len(path))
        pixels[path[pos]] = color
        if 0 <= old_pos < len(path):
            pixels[path[old_pos]] = BLACK


# while True:
#    print("Running")
#    color_fill(BLACK, 0)
#    travel_single(WHITE, 0.1)


print("Clearing LEDs.")
color_fill(BLACK, 0)
tick_move = 0  # advances each second, for walking
tick_move_last = 640
flickers_per_move = tick_move_dur / tick_flicker_dur
button6_down_already = not button6.value
running = True

while running and (tick_move <= tick_move_last):
    if tick_move >= tick_move_last:
        tick_move = 0
        color_fill(BLACK, 0)

    tick_flicker = 0

    # handle button6
    if (not button6.value and not button6_down_already):
        if running:
            running = False
        else:
            running = True
        print("running:", running)
        button6_down_already = True
        tick_move = 0
        color_fill(BLACK, 0)
    if button6.value:
        button6_down_already = False

    if running:
        print(tick_move, end=" ")
        # Jeff up
        rest(1, jeff, br1_2_to_br1_1)
        rest(1, maria, br1_4_to_lr2)
        walk(10, jeff, br1_2_to_br1_1)
        walk(16, jeff, br1_1_to_bath)
        walk(30, jeff, br1_1_to_bath, reverse=True)
        walk(40, jeff, br1_1_to_k1)
        loop(50, 3, jeff, k1_loop)
        # jeff deliver coffee
        walk(96, jeff, br1_4_to_k1, reverse=True)
        rest(117, maria, br1_4_to_k1)
        walk(115, jeff, br1_4_to_k1)
        # jeff make penny food
        loop(125, 1, jeff, k1_loop)
        walk(135, penny, br1_4_to_dr2)
        rest(137, maria, br1_4_to_k1)
        walk(150, jeff, k4_to_d4)
        walk(155, jeff, k4_to_d4, reverse=True)
        walk(156, penny, dr2_to_dr4)
        # penny out
        walk(170, penny, dr4_to_door2)
        walk(175, jeff, k4_to_door2)
        walk(180, jeff, k4_to_door2, reverse=True)
        # penny in then to bedroom
        walk(195, jeff, k4_to_door2)
        walk(200, jeff, k4_to_door2, reverse=True)
        loop(205, 2, jeff, k1_loop)
        walk(205, penny, b1_4_to_door2, reverse=True)
        rest(217, maria, br1_4_to_k1)
        # jeff eat breakfast
        walk(235, jeff, k4_to_d4)
        walk(280, jeff, k4_to_d4, reverse=True)
        # jeff workout in den
        walk(290, jeff, k4_to_d2)

        # Maria getting up
        walk(310, maria, br1_4_to_bath)
        walk(320, maria, br1_4_to_bath, reverse=True)
        # M to LR, fire on, then to kitchen
        walk(330, maria, br1_4_to_lr2)
        walk(394, maria, lr2_to_k4)
        # Penny to LR, M return
        walk(400, penny, br1_4_to_lr2)
        walk(410, maria, lr2_to_k4, reverse=True)
        # Jeff done workout; take shower
        walk(430, jeff, d2_to_bath)
        walk(470, jeff, br1_1_to_bath, reverse=True)
        # J to bedroom and closet getting dressed
        walk(490, jeff, br1_1_to_c2)
        walk(500, jeff, br1_1_to_c2, reverse=True)
        # Jeff to LR, then to work in guest room
        walk(505, jeff, br1_1_to_lr1)
        walk(560, jeff, lr1_to_b2_3)

        # Flickering
        while tick_flicker < flickers_per_move:
            # blink_board_light()
            tv_on(300, 425)
            fireplace(340, 640)
            # print(tick_move, tick_flicker)
            pixels.show()
            tick_flicker = tick_flicker + 1
            time.sleep(tick_flicker_dur)

        tick_move = tick_move + 1
