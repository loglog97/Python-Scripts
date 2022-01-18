from PIL import Image
from array import *
import cv2, os, sys, curses, time

"""
ASCII Picture and Video Converter
By: Logan Cole

Finished picture conversion: 7/24/2020
Finished video conversion: 7/24/2020
Finished Video playback: TBD
"""
asciiChars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
count = len(asciiChars)

#Converts the picture/frame to ascii characters
#returns the array containing ascii data
def toASCII(myImage):
    myImage = myImage.convert("L") #convert to gray
    codePic = '' 
    for i in range(0, myImage.size[1]):
        for j in range(0, myImage.size[0]):
            gray = myImage.getpixel((j, i)) #grabs pixel value from every pixel
            codePic = codePic + asciiChars[int(((count-1)*gray)/256)] #converts to an aciiChar
        codePic = codePic + "\n"
    return codePic

#converts an Image to ascii character, then prints to Command Line and File
def convertImage():
    fileName = input("Input file name: ")
    hratio = float(input("input height zoom ratio(default 1.0): ") or "1.0")
    wratio = float(input("input width zoom ratio(default 1.0): ") or "1.0")
    
    myImage = Image.open(fileName)
    myImage = myImage.resize((int(myImage.size[0]*wratio), int(myImage.size[1]*hratio))) #resize image
    file = open('result.txt','w')
    data = toASCII(myImage)
    print(data)
    file.write(data)
    file.close

#Converts a video frame by frame to ascii characters, prints each frame to a text document
def convertVideo():
    fileName = input("Input file name: ")
    hratio = float(input("input height zoon ratio(default 1.0): ") or "1.0")
    wratio = float(input("input width zoom ratio(default 1.0): ") or "1.0")
    capture = cv2.VideoCapture(fileName)
    i = 0
    if(os.path.isdir("./Video Out") == False): #looks for directory, if not there, it creates it
        os.makedirs("./Video Out")
    while(capture.isOpened()):
        ret, frame = capture.read() 
        if ret == False:
            break
        cv2.imshow('image', frame)
        k = cv2.waitKey(5)
        
        os.system('cls')
        i+=1
        
        tmp = open('./Video Out/frame('+str(i)+').txt', 'w')
        frame = cv2.resize(frame, (0,0), fx=wratio, fy=hratio) #resize individual frame
        frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #convert colors
        data = toASCII(frame) #convert to ascii
        print(data)
        tmp.write(data)
        tmp.close
        
        if(k & 0xff == ord('q')):
            break
        capture.release
        cv2.destroyAllWindows()

#Grabes each frame from the directory and attempts to play it back.
def playVideo():
    v = float(input("Frame per second: \t"))
    pmusic = input("play music?(y/n)\t")
    if(pmusic == 'y'):
        filedir = input("input music name:\t")
        thread = Thread(target = play_music, args = (filedir,))
        thread.start()
    stdscr = curses.initscr()
    stdscr.keypad(1)
    t0 = time.time()
    i = 1
    while(True):
        t1 = time.time()
        i = int((t1 - t0) * v) + 1
        filename = './Video Out/frame('+str(i)+')txt'
        try:
            with open(filename, 'r') as f:
                data = f.read()
                stdscr.addstr(0,0,data)
                stdscr.addstr("Frame: %d"%i)
                stdscr.refresh()
        except IOError:
            break
        
def main():
    ans = input("Convert Video or Picture?(v/p)\t")
    
    if(ans == 'v'): #If they want to convert a video
        convertVideo()
        playVideo()
    elif(ans == 'p'): #if they want to convert a picture
        convertImage()
    else:
        print("Invalid input. Shutting Down...")
        raise SystemExit


main()