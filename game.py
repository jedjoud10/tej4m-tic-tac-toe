# Importing common libraries for networking and camera
import socket
import os
from time import sleep
import struct
import ai
import numpy as np
#from picamera import PiCamera

# Constant private address of the host server to run the ML eval
address = "### ENTER PRIVATE SERVER IP"

# Port the socket will bind to
port = 25565
sock = socket.socket()
print("Trying to connect...")
sock.connect((address, port))
#camera = PiCamera()

# Const array of the states
unique_states = ['x', 'bg']

# Simple capture function that captures camera image
temp_image_path = "./image.jpg"
def capture():
        os.remove("./image.jpg")
        print("Capturing camera...")
        camera.capture(temp_image_path)
        print("Captured!")

# Checks the file stored in the temporary path 
def check():
        # Send the file size first
        file = open(temp_image_path, mode="br",)
        filesize = os.path.getsize(temp_image_path)
        sock.send(struct.pack("<Q", filesize))

        # Then send each individual chunk (1024 bytes = 1 chunk)
        print("Checking file: " + temp_image_path)
        while read_bytes := file.read(1024):
                sock.sendall(read_bytes)
        print("Sent all chunks... awaiting response")

        # Read back result from server and return state for each square in the grid
        sizeBytes = sock.recv(struct.calcsize("<9Q"))
        val = struct.unpack("<9Q", sizeBytes)
        print(np.asarray(val))
        return np.asarray(val)
currentBoard = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
while True:
        val = input("Awaiting player turn...")
        if val == "":
                # Get the positions where there would be Xs (as an array of 0s or 1s)
                predictions = check()
                
                for i in range(9):
                        x = i % 3
                        y = i // 3
                        if predictions[i] == 1:
                                currentBoard[y][x] = "2" 
                ai.takeTurn(currentBoard)
                ai.printBoard(currentBoard)

                isWin, Winner = ai.gameWon(currentBoard)
                if (isWin and Winner == 1):
                        print("dam")
                        break


        elif val == "q" or val == "Q":
                print("Thanks for playing!")