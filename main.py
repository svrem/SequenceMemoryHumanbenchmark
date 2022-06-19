from time import sleep
import mss
import numpy as np
import cv2
import pyautogui
import autoit
import keyboard


pyautogui.PAUSE = 0

STARTBUTTON = (1270, 520)
SLOW_MODE_ON_EVERY = 10
WHITE = (255, 255, 255)
monitor = {'top': 232, 'left': 1082, 'width': 380, 'height': 380}


sleep(1)
pyautogui.click(STARTBUTTON)
sleep(.1)


box_coords = []

box_size = monitor['width'] // 3

for y in range(0, 3):
    for x in range(0, 3):
        box_coords.append((x * box_size + box_size//2,
                          y * box_size + box_size//2))


def get_screen(sct):
    img = np.array(sct.grab(monitor))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def get_state(img, last_state):

    state = None
    while state == None or state == last_state and not keyboard.is_pressed('q'):
        img = get_screen(sct)

        for coord in box_coords:
            x, y = coord
            color = img[y, x]
            if (color == WHITE).all():
                state = box_coords.index(coord)
                break

    return state


def click_box(state, slow=False):
    x, y = box_coords[state]
    if (slow):
        autoit.mouse_click(
            x=monitor["left"]+x, y=monitor["top"]+y, speed=4)
    else:
        pyautogui.click(monitor["left"]+x, monitor["top"]+y)


with mss.mss() as sct:
    last_state = -1
    states = []
    level = 1

    while True:
        states = []
        last_state = -1
        for level_index in range(level):
            state = get_state(get_screen(sct), last_state)
            print(
                f"Recording {level_index+1}/{level}...                             ", end="\r")
            last_state = state
            states.append(state)
            sleep(.1)

        sleep(.4)

        for index, state in enumerate(states):
            print(
                f"Executing {index+1}/{level}...                             ", end="\r")
            click_box(state, level % SLOW_MODE_ON_EVERY == 0)
            # sleep(.1)

        level += 1
        sleep(1)
