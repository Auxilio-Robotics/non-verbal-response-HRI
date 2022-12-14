import numpy as np
import cv2
drawing = True # true if mouse is pressed
ix, iy = -1,-1

eyeRad = 150
eyesize = 512
desired_size = 750
def drawEyeLid(img, params, left = False):
    r, theta, arousal, valence = params
    if left:
        cv2.circle(img, (eyesize//2 - int(valence), int(arousal) * 4), eyesize, (0, 0, 0), -1)
    else:
        cv2.circle(img, (eyesize//2 + int(valence), int(arousal) * 4), eyesize, (0, 0, 0), -1)
    return img


mode = 'eyes'
def ballCallback(event,x,y,flags,param):
    global ballDrawPlane, mode, params
    dim = 200
    ballDrawPlane = np.zeros((dim,dim,3), np.uint8)
    cv2.line(ballDrawPlane, (dim//2, 0), (dim//2, dim), (255, 255, 255), 2)
    cv2.line(ballDrawPlane, (0, dim//2), (dim, dim//2), (255, 255, 255), 2)
    cv2.circle(ballDrawPlane,(x,y),10,(0,0,255),-1)
    r, theta = params['eyeloc'][:2]
    cv2.circle(ballDrawPlane, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), 10, (0, 255, 0), -1) # pupil
    if event == cv2.EVENT_MOUSEMOVE:
        if mode == 'eyes':
            r = np.sqrt((x - dim//2)**2 + (y- dim//2)**2) * 1.5
            theta = np.arctan2((y- dim//2), (x- dim//2))
            params['eyeloc'][0] = min(r, eyesize//2 - eyeRad)
            params['eyeloc'][1] = theta
        if mode == 'valencearousal':
            params[2] = (y - dim//2)
            params[3] = x - dim//2
        

def loadAsset(path, offset = (0, 0)):
    hh, ww = desired_size, desired_size
    bg = np.zeros((hh, ww, 3), np.uint8)
    alphas = np.zeros((hh, ww), np.uint8)
    img = cv2.imread(path, -1)
    h, w, _ = img.shape
    yoff = round((hh-h)/2) + offset[1]
    xoff = round((ww-w)/2) + offset[0]
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
    y1, x1 = y + offset[1], x + offset[0]
    y1 = np.clip(y1, 0, srcRGB.shape[1] - 1)
    x1 = np.clip(x1, 0, srcRGB.shape[0] - 1)
    srcRGB[y1, x1] = dstRGB[y, x]
    return srcRGB, np.clip(dstA + srcA, 0, 1)

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image.copy(), rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


def generateBall(iris, pupil, frac = 1, offset = (0, 0)):
    pa, pb = pupil
    pa = cv2.resize(pa, (0, 0), fx = frac, fy = frac, interpolation = cv2.INTER_NEAREST)
    pb = cv2.resize(pb, (0, 0), fx = frac, fy = frac, interpolation = cv2.INTER_NEAREST)
    
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
    global sclera, brow
    r, theta = params['eyeloc']
    viewLoc = np.array((r * np.cos(theta), r * np.sin(theta)))
    eyeball = generateBall(iris, pupil, 0.7, viewLoc)
    browloc = viewLoc / 4
    params['brow'][0] = np.mod(params['brow'][0] + 360, 360)

    # if params['brow'][0] <= 270:
    #     params['brow'][0] = 0

    r = params['brow'][1] + ( params['brow'][0] * 1.5 - 360)
    
    theta= params['brow'][0]

    browloc[0] += r * np.sin(-theta * np.pi/180)
    browloc[1] -= r * np.cos(-theta * np.pi/180)
    scleraLoc = viewLoc / 5
    ia = np.roll(sclera[0], int(scleraLoc[0]), 1)
    ib = np.roll(sclera[1], int(scleraLoc[0]), 1)
    ia = np.roll(ia, int(scleraLoc[1]), 0)
    ib = np.roll(ib, int(scleraLoc[1]), 0)
    sclera_temp = ia, ib
    finalimg = blend(sclera_temp, eyeball, viewLoc)
    
    brow_temp = rotate_image(brow[0], params['brow'][0]), rotate_image(brow[1], params['brow'][0])
    img, alpha = blend(finalimg, brow_temp, browloc)
    
    mask = cv2.inRange(img, np.array([-1, -1, -1]), np.array([1, 1, 1]))
    img[mask > 0] = [138, 207, 255]
    return img

def browCallback(event,x,y,flags,param):
    dim = 200
    browDrawPlane = np.zeros((dim,dim,3), np.uint8)
    cv2.line(browDrawPlane, (dim//2, 0), (dim//2, dim), (255, 255, 255), 2)
    cv2.line(browDrawPlane, (0, dim//2), (dim, dim//2), (255, 255, 255), 2)
    cv2.circle(browDrawPlane,(x,y),10,(0,0,255),-1)
    r, theta = params['eyeloc'][:2]
    cv2.circle(browDrawPlane, (dim//2 + int(r * np.cos(theta)) , dim//2 + int(r * np.sin(theta)) ), 10, (0, 255, 0), -1) # pupil
    dim = 200
    if event == cv2.EVENT_MOUSEMOVE:
        params['brow'][0] =  - (x ) / 4
        params['brow'][1] = 200 - y

brow = loadAsset('../images/parts/brow.png')
iris = loadAsset('../images/parts/iris.png', )
pupil = loadAsset('../images/parts/pupil.png', )
sclera = loadAsset('../images/parts/sclera.png', )
ulid = loadAsset('../images/parts/upperlid.png')
llid = loadAsset('../images/parts/lowerlid.png')


cv2.namedWindow('ballDrawPlane')
cv2.setMouseCallback('ballDrawPlane',ballCallback)

cv2.namedWindow('browDrawPlane')
cv2.setMouseCallback('browDrawPlane',browCallback)


ballDrawPlane = np.zeros((200,200,3), np.uint8)
browDrawPlane = np.zeros((200,200,3), np.uint8)
params = {'eyeloc' : [0, 0], 'brow' : [-0, 0]}
inc = 10
while(1):
    cv2.imshow('ballDrawPlane', ballDrawPlane)
    cv2.imshow('browDrawPlane', browDrawPlane)
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
    