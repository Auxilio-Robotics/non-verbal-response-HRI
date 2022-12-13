import numpy as np
import cv2
drawing = True # true if mouse is pressed
ix, iy = -1,-1

eyeRad = 85
dim = 512
def drawSingleEye(img, params):
    r, theta = params

    eyemask = img.copy()
    cv2.circle(eyemask, (dim//2, dim//2), dim//2, (0, 0, 0), -1)

    cv2.circle(img, (dim//2, dim//2), dim//2, (255, 255, 255), -1) # white eye
    cv2.circle(img, (dim//2, dim//2), dim//2, (0, 0, 0), 3) # white eye
    cv2.circle(img, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), eyeRad, (0, 0, 0), -1) # pupil
    img[eyemask == 255] = 255

    return img


def drawLoc(event,x,y,flags,param):
    global ix,iy,drawing, img
    img = np.zeros((512,512,3), np.uint8)
    if event == cv2.EVENT_MOUSEMOVE:
        r = np.sqrt((x - dim//2)**2 + (y- dim//2)**2)
        theta = np.arctan2((y- dim//2), (x- dim//2))
        params[0] = min(r, dim//2 - eyeRad)
        params[1] = theta

        cv2.line(img, (dim//2, 0), (dim//2, dim), (255, 255, 255), 2)
        cv2.line(img, (0, dim//2), (dim, dim//2), (255, 255, 255), 2)
        cv2.circle(img,(x,y),10,(0,0,255),-1)

cv2.namedWindow('image')
cv2.setMouseCallback('image',drawLoc)
img = np.zeros((dim,dim,3), np.uint8)

params = np.zeros((2,), float)
while(1):
    cv2.imshow('image', img)
    eye = np.ones((dim, dim, 3), np.uint8)*255
    eye = drawSingleEye(eye, params)
    eye = np.hstack([eye, eye])
    cv2.imshow('a', eye)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break