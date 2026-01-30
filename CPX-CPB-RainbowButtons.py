import time
import board
import digitalio
import neopixel
from rainbowio import colorwheel

NUM_PIXELS = 10

pixels = neopixel.NeoPixel(
    board.NEOPIXEL, NUM_PIXELS, brightness=0.3, auto_write=False
)

# --------------------
# Buttons
# --------------------
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)

button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

# --------------------
# Colors for first half
# --------------------
COLORS_FIRST = [
    (255, 0, 0),    # RED
    (255, 150, 0),  # YELLOW
    (0, 255, 0),    # GREEN
    (0, 255, 255),  # CYAN
]

# Colors for second half
COLORS_SECOND = [
    (0, 0, 255),    # BLUE
    (180, 0, 255),  # PURPLE
    (255, 255, 255),# WHITE
    (0, 0, 0)       # OFF
]

offset = 0
chase_step = 0
color_index = 0

# --------------------
# Main loop
# --------------------
while True:
    a_pressed = button_a.value
    b_pressed = button_b.value

    if a_pressed and b_pressed:
        # BOTH pressed → full code (combine first + second)
        current_colors = COLORS_FIRST + COLORS_SECOND
    elif a_pressed:
        current_colors = COLORS_FIRST
    elif b_pressed:
        current_colors = COLORS_SECOND
    else:
        # No buttons → turn off
        pixels.fill((0, 0, 0))
        pixels.show()
        chase_step = 0
        color_index = 0
        offset = 0
        time.sleep(0.02)
        continue

    # --------------------
    # Color Chase
    # --------------------
    pixels.fill((0, 0, 0))
    pixels[chase_step] = current_colors[color_index]
    chase_step = (chase_step + 1) % NUM_PIXELS
    if chase_step == 0:
        color_index = (color_index + 1) % len(current_colors)

    # --------------------
    # Rainbow overlay
    # --------------------
    for i in range(NUM_PIXELS):
        pixels[i] = colorwheel((i * 20 + offset) & 255)

    offset = (offset + 3) % 256
    pixels.show()
    time.sleep(0.03)
