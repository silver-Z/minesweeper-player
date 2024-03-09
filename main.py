from window_manger import *
from digital_recognizer import *
from board_recognizer import *
import cv2
import numpy as np

# Load the model
model = load_model()

# Get the game
window_id = get_window_id("Minesweeper")  # Replace with the actual window ID
if window_id is None:
    print("Could not find the game window")
    exit()
cgimage = capture_window(window_id)
save_cgimage_to_path(cgimage, 'assets/game.png')

# Recognize the board
image = cv2.imread("assets/game.png")
board = recognize_board(image)

# Recognize the level
level = recognize_level(image)

# Split the board
width = 0
height = 0

match level:
    case "Easy":
        width = 9
        height = 9
    case "Hard":
        width = 16
        height = 16
    case "Expert":
        width = 30
        height = 16
    case _:
        print("Unknown level")
        exit()

# Split the board into cells
cells = np.zeros((height, width), dtype="int8")

step_x = board.shape[1] // width
step_y = board.shape[0] // height

# Recognize the cells
for i in range(height):
    for j in range(width):
        cell = board[i*step_y:(i+1)*step_y, j*step_x:(j+1)*step_x]
        digit = extract_digit(cell, model)
        if digit is not None:
            cells[i, j] = digit[0]

print(cells)