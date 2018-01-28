import numpy as np


def get_equiv(equivlence):
    for i in reversed(list(equivlence)):
        for j in equivlence[i]:
            if equivlence[j]:
                equivlence[i] = list(set(equivlence[i] + equivlence[j]))
    # print equivlence
    label = [i for i in equivlence]

    seg = {}
    while label:
        a = label.pop(0)
        for i in equivlence[a]:
            seg[i] = a
            if i in label: label.pop(label.index(i))
    return seg

##################### Image segementing by 8 connected ############
def get_8connected(thresh):
    h,w=thresh.shape
    image_label = np.zeros((h,w), dtype=np.int)
    label = 0
    equivlence = {}
    for i in range(h):
        for j in range(w):
            # if i == 83 and j == 1980:
            #     print
            if thresh[i,j] == 255:
                if i != 0 and j > 0 and j < w-1 :
                    if int(thresh[i - 1, j - 1]) + thresh[i - 1, j] + thresh[i - 1, j + 1] + thresh[i, j - 1] == 0:
                        label += 1
                        equivlence[label] = []
                        image_label[i,j] = label
                    else:
                        l = sorted(list(set([image_label[i - 1, j - 1], image_label[i - 1, j], image_label[i - 1, j + 1], image_label[i, j - 1]])))
                        if l[0] == 0: l.pop(0)
                        try:
                            image_label[i, j] = l[0]
                        except IndexError:
                            print "label error !!!!!!!!!!!",i,j
                        if len(l) > 1:
                            equivlence[l[0]] = list(set(equivlence[l[0]] + l[1:]))
                elif j==0:
                    if int(thresh[i - 1, j]) + thresh[i - 1, j + 1] == 0:
                        label += 1
                        equivlence[label] = []
                        image_label[i, j] = label
                    elif image_label[i - 1, j] == 0:
                        image_label[i, j] = image_label[i - 1, j + 1]
                    elif image_label[i - 1, j + 1] == 0:
                        image_label[i, j] = image_label[i - 1, j + 1]
                    else:
                        if thresh[i - 1, j] == thresh[i - 1, j + 1]:
                            image_label[i, j] = image_label[i - 1, j + 1]
                        else:
                            image_label[i, j] = image_label[i - 1, j]
                            equivlence[image_label[i - 1, j]] = list(set(equivlence[image_label[i - 1, j]]+[image_label[i - 1, j+1]]))
                elif i==0:
                    if thresh[i, j - 1] == 255:
                        image_label[i, j] = image_label[i,j-1]
                    else:
                        label += 1
                        equivlence[label] = []
                        image_label[i, j] = label
                elif j == w-1 and i != 0:
                    if int(thresh[i - 1, j - 1]) + thresh[i - 1, j] + thresh[i, j - 1] == 0:
                        label += 1
                        equivlence[label] = []
                        image_label[i,j] = label
                    else:
                        l = sorted(list(set([image_label[i - 1, j - 1], image_label[i - 1, j], image_label[i, j - 1]])))
                        if l[0] == 0: l.pop(0)
                        if not l:
                            continue
                        try:
                            image_label[i, j] = l[0]
                        except IndexError:
                            print "label error !!!!!!!!!!!",i,j
                        if len(l) > 1:
                            equivlence[l[0]] = list(set(equivlence[l[0]] + l[1:]))
    seg = get_equiv(equivlence)
    # print "seg :",seg
    for i in range(h):
        for j in range(w):
            if image_label[i,j]:
                if image_label[i,j] in seg:
                    image_label[i,j] = seg[image_label[i,j]]
    return image_label
########################################################################################

if __name__ == "__main__":
    thresh = np.array(
        [
            [0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [255, 255, 255, 255, 0, 0, 255, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0, 255, 0, 255],
            [255, 255, 255, 255, 255, 0, 255, 255, 255, 0, 0, 0, 0, 0, 255, 255, 255, 255, 0, 255, 0, 0],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 255, 0],
            [0, 0, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 255, 255],
            [0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 0, 0, 0, 255, 0],
            [0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 0, 0, 0, 255, 255],
            [0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [255, 255, 255, 255, 0, 0, 255, 0, 0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0],
            [255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 0],
            [255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 0, 0, 0, 0],
            [0, 0, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 255, 0, 0, 255, 255, 255, 0, 0, 0, 0],
            [0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 255, 255],
            [0, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 0, 0, 0, 255, 255],
            [0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255],
        ]
        , dtype=np.uint8
    )
    print get_8connected(thresh)