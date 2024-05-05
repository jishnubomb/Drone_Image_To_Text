# Importing necessary libraries
from djitellopy import Tello  # Library for controlling Tello drone
import cv2 as cv  # OpenCV library for computer vision tasks
from PIL import Image  # Library for handling images
from pytesseract import pytesseract  # Python wrapper for Tesseract OCR engine

# Reading position data from mission.txt file
with open('mission.txt') as position:
    position_data = position.readlines()
    position_data_list = position_data[0].split(",")
    print(position_data_list)
    # Extracting position data
    x = int(position_data_list[0])  # x-coordinate
    y = int(position_data_list[1])  # y-coordinate
    z = int(position_data_list[2])  # z-coordinate
    cw = int(position_data_list[3])  # Clockwise rotation angle
    key = int(position_data_list[4])  # Encryption key
    position.close()

# Initializing Tello drone
tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()
print(tello.get_battery())  # Displaying battery level
tello.takeoff()  # Taking off
tello.rotate_clockwise(cw)  # Rotating clockwise
tello.move_forward(x)  # Moving forward
tello.move_left(y)  # Moving left
tello.move_up(z-50)  # Moving up (subtracting 50 from z-coordinate)
frame_read = tello.get_frame_read()

# Capturing frame and saving it as picture.png
cv.imwrite("picture.png", frame_read.frame)

tello.land()  # Landing the drone

# Setting up Tesseract OCR
path_to_tesseract = r'C:\Users\chint\anaconda3\envs\tello\Lib\site-packages\tesseract.exe'
path_to_image = r'C:\Users\chint\picture.png'
pytesseract.tesseract_cmd = path_to_tesseract

# Opening the image using PIL
img = Image.open(path_to_image)

# Performing OCR on the image
text = pytesseract.image_to_string(img)

# Function to encrypt text using Caesar Cipher
def encrypt(text, s):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if (char.isupper()):
            result += chr((ord(char) + s - 65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result[:-1]  # Removing the last character

# Writing encrypted text to result.txt file
with open('result.txt', 'w') as code:
    code.write(encrypt(text, key))
