import cv2
import pickle
import numpy as np

def checkParkSpace(imgg):
    spaceCounter = 0
    
    for pos in posList:
        x,y = pos
        imgCrop = imgg[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)
        
        
        if count < 150:
            color = (0,255,0)
            thickness = 2
            spaceCounter +=1
        else:
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img, pos, (pos[0] + width,pos[1]+height),color,thickness)
        cv2.putText(img,str(count) ,(x,y+height-2), cv2.FONT_HERSHEY_PLAIN, 1, color)

    cv2.putText(img, f"Free: {spaceCounter}/{len(posList)}", (15,24), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,255),4)    
        
        
width = 27
height = 15

cap = cv2.VideoCapture("video.mp4")


with open("CarParkpos","rb") as f:
    posList = pickle.load(f)
    

while True:
    
    success ,img = cap.read()
    if not success:
        break
    imgGRAY = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGRAY,(3,3), 1)
    imgThreshhold = cv2.adaptiveThreshold(imgBlur, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshhold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)),iterations=1)
    
    
    checkParkSpace(imgDilate)
    cv2.imshow("img",img)
    
    
    k = cv2.waitKey(200) & 0xFF
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()

cv2.destroyAllWindows()