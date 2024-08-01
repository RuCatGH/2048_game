import pyautogui


def swipe_up(start_x: int, start_y: int, offset: int, duration=0.1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(start_x, start_y-offset, duration=duration, button='left')


def swipe_down(start_x: int, start_y: int, offset: int, duration=0.1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(start_x, start_y+offset, duration=duration, button='left')


def swipe_left(start_x: int, start_y: int, offset: int, duration=0.1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(start_x-offset, start_y, duration=duration, button='left')


def swipe_right(start_x: int, start_y: int, offset: int, duration=0.1):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(start_x+offset, start_y, duration=duration, button='left')
