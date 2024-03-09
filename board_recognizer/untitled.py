import cv2
import pytesseract

def recognize_level(img):
    img = img[85:130, 50:160]
    
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to recognize the text
    text = pytesseract.image_to_string(gray)

    # Check the recognized text and return the level
    if 'easy' in text.lower():
        return 'Easy'
    elif 'hard' in text.lower():
        return 'Hard'
    elif 'expert' in text.lower():
        return 'Expert'
    else:
        return 'Unknown'
    
def recognize_board(img):
    img = img[290:-30, 30:-30]
    return img

# image = cv2.imread("assets/game.png")
# cv2.imshow("Board", recognize_board(image))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# level = recognize_level(img=image)
# print(level)