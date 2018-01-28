import numpy as np, cv2, os
from threshold import otsu_threshold
from _8connected import get_8connected
from Area import areaThreshold_by_havg

def segment_image(img_file, exp=3):
    org = cv2.imread(img_file,cv2.IMREAD_COLOR)

    h, w = org.shape[:2]

    # removing noise by using Non-local Means Denoising algorithm
    img = cv2.fastNlMeansDenoisingColored(org,None,10,10,7,21)
    # cv2.imshow('cleaned',img)

    # Taking the red component out of RBG image as it is less effected by shadow of grain or impurity
    gray = np.array([[img[i,j,2] for j in range(w)]for i in range(h)])

    # calculating threshold value by using otsu thresholding
    T = otsu_threshold(gray=gray)

    # incresing contrast about the threshold
    # img = np.array([[max(pixel - 25, 0) if pixel < T else min(pixel + 25, 255) for pixel in row] for row in gray], dtype=np.uint8)
    # cv2.imshow('contrast',img)

    # generating a threshold image
    thresh = np.array([[0 if gray[i,j]<T else 255 for j in range(w)]for i in range(h)], dtype=np.uint8)
    # cv2.imshow('thresh',thresh)

    # generating a mask using 8-connected component method on threshold image
    mask = get_8connected(thresh)

    # Calcutaing the grain segment using mask image
    s = {}
    for i in range(h):
        for j in range(w):
            if mask[i,j]:
                if mask[i,j] in s:
                    if i < s[mask[i,j]][0]: s[mask[i, j]][0] = i
                    elif i > s[mask[i,j]][1]: s[mask[i, j]][1] = i
                    elif j < s[mask[i,j]][2]: s[mask[i, j]][2] = j
                    elif j > s[mask[i,j]][3]: s[mask[i, j]][3] = j
                else:
                    s[mask[i,j]] = [i,i,j,j]

    # removing the backgraound of grain
    torg = np.array([[[0,0,0] if mask[i,j] == 0 else org[i,j] for j in range(w)] for i in range(h)], dtype=np.uint8)

    low_Tarea, up_Tarea = areaThreshold_by_havg(s, exp=exp)
    # grnerating the segmented image
    # for i in s:
    #     if s[i][0]-s[i][1] and s[i][2]-s[i][3]:
    #         torg = cv2.rectangle(torg, (s[i][2],s[i][0]), (s[i][3],s[i][1]), (0, 0, 255), 1)
    # cv2.imshow('segmented', torg)

    # calculating the segments
    segments = {}
    # rect = torg.copy()
    for i in s:
        area = (s[i][0] - s[i][1]) * (s[i][2] - s[i][3])
        if area > low_Tarea and area < up_Tarea:
            # rect = cv2.rectangle(rect, (s[i][2], s[i][0]), (s[i][3], s[i][1]), (0, 0, 255), 1)
            segments[i] = torg[s[i][0]:s[i][1],s[i][2]:s[i][3]]

    # cv2.imwrite( "result_image.jpg", rect);
    return segments, s

def get_files(indir):
    indir = indir.rstrip('/')
    flist =os.listdir(indir)
    files = []
    for f in flist:
        f = indir+'/'+f
        if os.path.isdir(f):
            tfiles = get_files(f)
            files += [tf for tf in tfiles]
        else:
            files.append(f)
    return files


# if __name__=="__main__":
#     in_dir = '/media/zero/41FF48D81730BD9B/wheat/Grain/'
#     out_dir = '/media/zero/41FF48D81730BD9B/wheat/dataset/'
#     count = 1
#     files = get_files(in_dir)
#     for img in files:
#         print img+' is processing...'
#         segments, _ = segment_image(img)
#         print "\tprocessing complete......... contain %d segments"%(len(segments))
#         for i in segments:
#             odir = out_dir+'/'.join(img.split('.')[:-1])[len(in_dir):]+'_'
#             cv2.imwrite(odir+str(count)+'.jpg', segments[i])
#             count+=1