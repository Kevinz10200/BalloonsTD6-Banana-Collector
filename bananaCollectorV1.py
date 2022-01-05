import pyautogui
pyautogui.PAUSE = 0.01 # how long between each keystroke command
import cv2
import numpy as np
import time
from imutils.object_detection import non_max_suppression
from pynput.mouse import Button, Controller

def importImages(): #maybe add names for input() hereo
    farm000 = cv2.imread("farm000.JPG")
    farm100 = cv2.imread("farm100.JPG")
    farm200 = cv2.imread("farm200.JPG")
    farm300 = cv2.imread("farm300.JPG")
    farm400 = cv2.imread("farm400.JPG")
    farm210 = cv2.imread("farm210.JPG")
    farm320 = cv2.imread("farm320.JPG")
    farm220 = cv2.imread("farm220.JPG")
    
    #returns all bananaFarm images as list [cv2 image obj]
    return [farm000, farm100, farm200, farm300, farm400, farm210, farm320, farm220]

#this version takes a list of potential objects to be found in canvas
def matchSprite(canvas, potentialMatches): # return list [tuple<minVal, maxVal, tuple maxLocation <x, y>, tuple minLocation <x, y>>]
    #minval is the darkest spot, the worst match
    #maxVal is the brightest spot, the best match
    #locations are stored as 2tuples indicating coordinates of top left pixel
    
    finalLocations = []
    rects = []
    for farm in potentialMatches:
        result = cv2.matchTemplate(canvas, farm, cv2.TM_CCOEFF_NORMED)
        (xnew, ynew) = np.where(result >= 0.72)
        #print(f"[DEBUG] {len(ynew)} matched locations *before* NMS")
        
        for (x,y) in zip(xnew, ynew):
            rects.append((x, y, x + 90, y + 90)) # width of bounding box is 90
        
        #print(f"[DEBUG] {len(culled)} matched locations *after* NMS")
        #print()
        
    culled = non_max_suppression(np.array(rects)) # cull duplicate bounding boxes via NMS 
    
    return culled 
    # array of coords in the format topx, topy, botx, boty to be unpacked
    # indicating topleft and bottom right corner of bounding boxes

# takes a list of 2tuples indicating (top left) position(s) of farm(s)
def collectBanana(x, y): # moves cursor to collect bananas 
    "to do list: only move cursor if no input has been detected for some time to avoid taking over"
    # record mouse pos so cursor pos gets returned to after collection
    mouse = Controller()
    # read pointer position
    savedMousePos = mouse.position
    #takes 2 locations x, y, specifiying where to move cursor to
    pyautogui.moveTo(x, y)
    # return mouse to previous pos
    mouse.position = savedMousePos
    
# confidence threshhold at 0.84
def runOnce(debug=False): 
    noFarms = True
    canvas = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2RGB) #take SS store as canvas
    farmLib = importImages() #list of possible farm imgs
    
    databank = matchSprite(canvas, farmLib) #minVal, maxVal, minLoc, maxLoc
    #print(databank)
    #print()
        
    #debugText = "[DEBUG READOUT]"
    if (debug):
        #build debug readout txt
        pass
    for (topx, topy, botx, boty) in databank:
        noFarms = False
        collectBanana(topy+40, topx+40)
    
    if(debug):
        #print(debugText)
        for (topx, topy, botx, boty) in databank:
            cv2.rectangle(canvas, (topy, topx), (boty, botx), color=(0, 0, 255), thickness=6, lineType=cv2.LINE_4)
        canvas = cv2.resize(canvas, (2560, 1080))
        cv2.imshow("debug view", canvas)
        cv2.waitKey()
    
    return not noFarms
    # boolean indicating success or failure to find farms on screen

    
        
def bananaCollectorLoop(interval=10, debug=False):
    # setup code
    # bananas expire every 15 seconds
    # timekeeping
    starttime = time.time() 
    
    while True:
        print("\nChecking if idle")
        #if (checkIfIdle()):
        
        print("\nLoooking for bananas...")
        if(runOnce(debug=debug)):
            print(f" Bananas collected; will run again in {interval} seconds.")
        else:
            print(f" No farms, Will try again in {interval} seconds.")
        time.sleep(interval - ((time.time() - starttime) % interval))
        


def checkIfIdle(): # returns bool for if user is idle
    pass


if __name__ == "__main__":
    
    """To remove duplicate bounding boxes, apply NMS to entire array, perhaps store every coord as a single array of coords
    rather than as an array of tuples for each loop. Apply NMS once at the end of loop or once every loop"""
    
    print('where banana')
    print('- - -')
    
    #runOnce(debug=False)
    # bananas expire every 15 seconds
    interval = 5
    debug = False
    bananaCollectorLoop(interval=interval, debug=debug)
    
    
    
    