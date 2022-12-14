import numpy as np
import cv2
drawing = True # true if mouse is pressed
ix, iy = -1,-1

eyeRad = 150
eyesize = 512

def drawEyeLid(img, params, left = False):
    r, theta, arousal, valence = params
    if left:
        cv2.circle(img, (eyesize//2 - int(valence), int(arousal) * 4), eyesize, (0, 0, 0), -1)
    else:
        cv2.circle(img, (eyesize//2 + int(valence), int(arousal) * 4), eyesize, (0, 0, 0), -1)
    return img


mode = 'eyes'
def drawLoc(event,x,y,flags,param):
    global drawPlane1, mode, params
    dim = 200
    drawPlane1 = np.zeros((200,200,3), np.uint8)
    cv2.line(drawPlane1, (dim//2, 0), (dim//2, dim), (255, 255, 255), 2)
    cv2.line(drawPlane1, (0, dim//2), (dim, dim//2), (255, 255, 255), 2)
    cv2.circle(drawPlane1,(x,y),10,(0,0,255),-1)
    r, theta = params[:2]
    cv2.circle(drawPlane1, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), 10, (0, 255, 0), -1) # pupil

    cv2.circle(drawPlane1, (int(params[3] * dim /np.pi)  + dim//2 , int(params[2])), 10, (0, 0, 255), -1) # pupil


    if event == cv2.EVENT_MOUSEMOVE:
        if mode == 'eyes':
            r = np.sqrt((x - dim//2)**2 + (y- dim//2)**2) 
            theta = np.arctan2((y- dim//2), (x- dim//2))
            params[0] = min(r, eyesize//2 - eyeRad)
            params[1] = theta
        if mode == 'valencearousal':
            params[2] = (y - dim//2)
            params[3] = x - dim//2
        

def loadAsset(path):
    hh, ww = 650, 650
    bg = np.zeros((hh, ww, 3), np.uint8)
    alphas = np.zeros((hh, ww), np.uint8)
    img = cv2.imread(path, -1)
    h, w, _ = img.shape
    yoff = round((hh-h)/2)
    xoff = round((ww-w)/2)
    im = img[:, :, :3]
    alpha = img[:, :, 3]
    im[alpha == 0] = 0
    bg[yoff:yoff + h, xoff:xoff + w] = im
    alphas[yoff:yoff + h, xoff:xoff + w] = alpha
    return bg, alphas
    
def blend(im1, im2, offset = (0, 0)):
    offset = np.array(offset, int)
    srcRGB = im1[0].copy()
    dstRGB = im2[0].copy()
    srcA = im1[1].copy()
    dstA = im2[1].copy()
    y, x = np.where(dstA > 0)
    srcRGB[y + offset[1], x + offset[0]] = dstRGB[y, x]
    return srcRGB, np.clip(dstA + srcA, 0, 1)

def generateBall(iris, pupil, frac = 1, offset = (0, 0)):
    pa, pb = pupil
    pa = cv2.resize(pa, (0, 0), fx = frac, fy = frac, interpolation = cv2.INTER_NEAREST)
    pb = cv2.resize(pb, (0, 0), fx = frac, fy = frac, interpolation = cv2.INTER_NEAREST)
    desired_size = 650
    new_size = pa.shape
    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    pa = cv2.copyMakeBorder(pa, top, bottom, left, right, cv2.BORDER_CONSTANT)
    pb = cv2.copyMakeBorder(pb, top, bottom, left, right, cv2.BORDER_CONSTANT)
    pup = pa, pb
    eyeball = blend(iris, pup, (np.array(offset)/4.0).astype(int))
    return eyeball


def renderEye(params):
    viewLoc = (params[0] * np.cos(params[1]), params[0] * np.sin(params[1]))
    eyeball = generateBall(iris, pupil, 0.7, viewLoc)
    finalimg = blend(sclera, eyeball, viewLoc)
    return finalimg[0]

drawPlane1 = np.zeros((eyesize,eyesize,3), np.uint8)


brow = loadAsset('../images/parts/brow.png')
iris = loadAsset('../images/parts/iris.png')
pupil = loadAsset('../images/parts/pupil.png')
sclera = loadAsset('../images/parts/sclera.png')
ulid = loadAsset('../images/parts/upperlid.png')
llid = loadAsset('../images/parts/lowerlid.png')


cv2.namedWindow('drawPlane1')
cv2.setMouseCallback('drawPlane1',drawLoc)



params = np.zeros((4,), float)
inc = 10
while(1):
    cv2.imshow('drawPlane1', drawPlane1)
    eye = renderEye(params)
    # eye = np.hstack([eye, eye])
    cv2.imshow('a', eye)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('v'):
        mode = 'valencearousal'
    elif k == ord('e'):
        mode = 'eyes'
    