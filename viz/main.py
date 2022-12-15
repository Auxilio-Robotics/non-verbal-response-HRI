import numpy as np
import cv2
drawing = True # true if mouse is pressed
ix, iy = -1,-1

eyeRad = 85
dim = 512

def drawPupil(img, params):
    r, theta, arousal, valence = params

    eyemask = img.copy()
    cv2.circle(eyemask, (dim//2, dim//2), dim//2, (0, 0, 0), -1)

    cv2.circle(img, (dim//2, dim//2), dim//2, (255, 255, 255), -1) # white eye
    cv2.circle(img, (dim//2, dim//2), dim//2, (0, 0, 0), 3) # white eye
    cv2.circle(img, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), eyeRad, (0, 0, 0), -1) # pupil
    return img

def drawEyes(params):
    
    img = np.zeros((512,512,3), np.uint8) * 255
    limg = drawPupil(img.copy(), params)
    rimg = drawPupil(img.copy(), params)
    limg = drawEyeLid(limg, params, True)
    rimg = drawEyeLid(rimg, params, False)

    eyemask = img.copy()
    cv2.circle(eyemask, (dim//2, dim//2), dim//2, (0, 0, 0), -1)
    limg[eyemask == 255] = 255
    rimg[eyemask == 255] = 255

    return np.hstack([limg, rimg])
    

def drawEyeLid(img, params, left = False):
    r, theta, arousal, valence = params
    if left:
        cv2.circle(img, (dim//2 - int(valence), int(arousal) * 4), dim, (0, 0, 0), -1)
    else:
        cv2.circle(img, (dim//2 + int(valence), int(arousal) * 4), dim, (0, 0, 0), -1)
    return img

    



mode = 'eyes'
def drawLoc(event,x,y,flags,param):
    global img, mode, params
    img = np.zeros((512,512,3), np.uint8)
    cv2.line(img, (dim//2, 0), (dim//2, dim), (255, 255, 255), 2)
    cv2.line(img, (0, dim//2), (dim, dim//2), (255, 255, 255), 2)
    cv2.circle(img,(x,y),10,(0,0,255),-1)
    r, theta = params[:2]
    cv2.circle(img, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), 10, (0, 255, 0), -1) # pupil

    cv2.circle(img, (int(params[3] * dim /np.pi)  + dim//2 , int(params[2])), 10, (0, 0, 255), -1) # pupil


    if event == cv2.EVENT_MOUSEMOVE:
        if mode == 'eyes':
            r = np.sqrt((x - dim//2)**2 + (y- dim//2)**2)
            theta = np.arctan2((y- dim//2), (x- dim//2))
            params[0] = min(r, dim//2 - eyeRad)
            params[1] = theta
        if mode == 'valencearousal':
            params[2] = (y - dim//2)
            params[3] = x - dim//2
        

cv2.namedWindow('image')
cv2.setMouseCallback('image',drawLoc)
img = np.zeros((dim,dim,3), np.uint8)

params = np.zeros((4,), float)
params[0] = 0
params[1] = 0
params[2] = dim//2
params[3] = dim//2
inc = 10
while(1):
    cv2.imshow('image', img)
    eye = drawEyes(params)
    # eye = np.hstack([eye, eye])
    cv2.imshow('a', eye)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('v'):
        mode = 'valencearousal'
    elif k == ord('e'):
        mode = 'eyes'
    