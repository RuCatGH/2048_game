from detect import get_board_2048
from ai.solver_2048 import ai_play
from game_moves import swipe_down, swipe_left, swipe_right, swipe_up
import time


def main():
    move_number = 500
    while True:
        board, center_x, center_y = get_board_2048()
        print('NEYRO', board)
        move_number += 1
        best_move = ai_play(board, move_number)

        offset = 50
        duration = 0.3
        match best_move:
            case 'move_up':
                swipe_up(center_x, center_y, offset, duration)
            case 'move_down':
                swipe_down(center_x, center_y, offset, duration)
            case 'move_left':
                swipe_left(center_x, center_y, offset, duration)
            case 'move_right':
                swipe_right(center_x, center_y, offset, duration)
        time.sleep(1)


if __name__ == "__main__":
    main()
