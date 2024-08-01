import pygetwindow as gw
import pyautogui
import numpy as np
import cv2
import time
from ai.number_detect import get_number_from_image
import os


class GameWindow:
    def __init__(self, title):
        self.game_win = gw.getWindowsWithTitle(title)[0]

    def capture_screen(self):
        try:
            self.game_win.restore()
            self.game_win.activate()

            win_left, win_top, win_width, win_height = self.game_win.left, self.game_win.top, self.game_win.width, self.game_win.height
            screen = np.array(pyautogui.screenshot(
                region=(win_left, win_top, win_width, win_height)))
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

            center_x = win_left + win_width // 2
            center_y = win_top + win_height // 2

            return screen[450:-100:, :-50], center_x, center_y
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None, None, None


def threshold_tiles(board_img):
    hsv = cv2.cvtColor(board_img, cv2.COLOR_BGR2HSV)

    # Define the range for the background color in HSV
    board_bgd_color = np.array([26,  15, 241])

    # Define the range for the white color in HSV

    upper_white = np.array([0, 0, 255])

    # Create masks for the background color and white color
    mask_bgd = cv2.inRange(hsv, board_bgd_color, board_bgd_color)
    mask_white = cv2.inRange(hsv, upper_white, upper_white)

    # Combine the masks
    combined_mask = cv2.bitwise_or(mask_bgd, mask_white)

    # Apply dilation to the combined mask
    kernel = np.ones((10, 10), np.uint8)
    combined_mask = cv2.dilate(combined_mask, kernel)

    # Invert the mask to get the regions of interest
    return ~combined_mask


def get_box_contours(mask):
    cnt, hierarchy = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cnt = list(filter(lambda x: cv2.contourArea(x) > 100, cnt))

    return cnt


def y_alignment(contours):
    rectangles = []

    for i in range(0, len(contours), 4):
        x, y, w, h = cv2.boundingRect(contours[i])
        x2, y, w2, h2 = cv2.boundingRect(contours[i+1])
        x3, y, w3, h3 = cv2.boundingRect(contours[i+2])
        x4, y, w4, h4 = cv2.boundingRect(contours[i+3])
        rectangles.extend([[x, y, w, h], [x2, y, w2, h2],
                          [x3, y, w3, h3], [x4, y, w4, h4]])
    return sorted(rectangles, key=lambda x: (x[1], x[0]))


def get_board_2048():
    try:
        game_window_title = "LDPlayer-1"
        game_window = GameWindow(game_window_title)
        game_snapshot, center_x, center_y = game_window.capture_screen()

        if game_snapshot is not None:

            mask = threshold_tiles(game_snapshot)
            contours = get_box_contours(mask)
            contours = sorted(contours, key=lambda x: (
                cv2.boundingRect(x)[1], cv2.boundingRect(x)[0]))

            # cv2.imshow('mask', mask)
            # cv2.waitKey(0)
            roi_images = []
            for i, rectangle in enumerate(y_alignment(contours)):
                x, y, w, h = rectangle
                roi = game_snapshot[y:y+h, x:x+w]
                roi_images.append(roi)
                # cv2.drawContours(game_snapshot, contours, i, (0, 255, 0), 3)
                # cv2.imshow(f'ROI {i}', roi)
                # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            numbers = []

            for i, roi in enumerate(roi_images):
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                file_name = f'roi_{i}.jpg'
                cv2.imwrite(file_name, roi[20:-10, 10:-10])

                number = get_number_from_image(file_name)
                numbers.append(number)

                os.remove(file_name)

            return np.array(numbers).reshape(4, 4), center_x, center_y
    except Exception as ex:
        print(ex)
        time.sleep(1)
        return get_board_2048()


if __name__ == "__main__":
    rois = get_board_2048()
