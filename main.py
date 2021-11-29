import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)


## COLOR    -      BGR          -     MIN HSV       -       MAX HSV
## Blue     -   [255, 0, 0]     -   [90, 48, 0]     - [118, 255, 255] 
## Orange   -   [51, 153, 255]  -   [5, 107, 0]     - [19, 255, 255]
## Purple   -   [255, 0, 255]   -   [133, 56, 0]    - [159, 156, 255]
## Green    -   [0, 255, 0]     -   [57, 76, 0]     - [100, 255, 255]

class Color:
    def __init__(self, colorName, BGR, minHSV, maxHSV):
        self.colorName = colorName
        self.BGR = BGR
        self.minHSV = minHSV
        self.maxHSV = maxHSV
class Point:
    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.color = color

def addColor(colorName, BGR, minHSV, maxHSV, COLORS):
    newColor = Color(colorName, BGR, minHSV, maxHSV)
    COLORS.add(newColor)

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
    
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)

    if x == -1 and y == -1:
        return None
    return x+w // 2, y
 
def getColor(img, COLORS, OUTPUTIMG):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    i = 0
    Points= []
    for color in COLORS:
        lower = np.array(color.minHSV)
        upper = np.array(color.maxHSV)
        mask = cv2.inRange(imgHSV,lower,upper)

        x, y = getContours(mask)

        cv2.circle(OUTPUTIMG, (x,y), 15, color.BGR ,cv2.FILLED)
        if x!=0 and y!=0:
            point = Point(x, y, color)
            Points.append(point)
        i +=1
        
    return Points

def drawOnCanvas(Points, OUTPUTIMG):
    for point in Points:
        cv2.circle(OUTPUTIMG, (point.x, point.y), 10, point.color.BGR, cv2.FILLED)
    
 

COLORS = []

addColor("Blue", [255, 0, 0], [90, 48, 0], [118, 255, 255], COLORS)
addColor("Orange", [51, 153, 255], [5, 107, 0], [19, 255, 255], COLORS)
addColor("Purple", [255, 0, 255], [133, 56, 0], [159, 156, 255], COLORS)
addColor("Green", [0, 255, 0], [57, 76, 0], [100, 255, 255], COLORS)


while True:
    success, img = cap.read()
    OUTPUTIMG = img.copy()
    
    POINTS = getColor(img, COLORS, OUTPUTIMG)
    drawOnCanvas(POINTS, OUTPUTIMG)
    
    
    cv2.imshow("Result", img)
    
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break