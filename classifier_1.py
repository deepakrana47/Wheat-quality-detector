import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


import cv2, numpy as np, random
from segment_formation import get_files
from mlp import train
from PCA import pca

def make_sets(inputs, out, percent):
    if len(inputs) != len(out): print "Error input size not equal to output size !!!"
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    rang = range(len(inputs))
    random.shuffle(rang)
    for i in rang:
        if random.random() < percent:
            x_test.append(inputs[i])
            y_test.append(out[i])
        else:
            x_train.append(inputs[i])
            y_train.append(out[i])
    return x_train, y_train, x_test, y_test

if __name__ == "__main__":
    grain = './dataset_2/grain'
    impure = './dataset_2/impurities'
    impurity_list = get_files(impure)
    grain_list = get_files(grain)
    colorIn = grain_list + impurity_list
    out = [[1,0] for i in range(len(grain_list))] + [[0,1] for i in range(len(impurity_list))]
    x_train, y_train, x_test, y_test = make_sets(colorIn, out, 0.1)

    xgtrain = []
    xctrain = []
    for g in x_train:
        img = cv2.imread(g, cv2.IMREAD_COLOR)
        xctrain.append(img)
        xgtrain.append(img[:, :, 2])

    xgtest = []
    xctest = []
    for i in x_test:
        img = cv2.imread(i, cv2.IMREAD_COLOR)
        xctest.append(img)
        xgtest.append(img[:, :, 2])

    print "Number of grain sample:", len(grain_list)
    print "Number of impurity sample:",len(impurity_list)
    print "Total of sample:",len(colorIn)

    # extracting features of grains
    ftrain = []
    for gi in range(len(xctrain)):
        gcolor = xctrain[gi]
        ggray = xgtrain[gi]
        h, w = ggray.shape
        area = np.sum(np.sum([[1.0 for j in range(w) if ggray[i,j]] for i in range(h)]))
        mean_area = area/(h*w)
        r, b, g = np.sum([gcolor[i,j] for j in range(gcolor.shape[1]) for i in range(gcolor.shape[0])], axis=0)/(area*256)
        _,_,eigen_value = pca(ggray)
        eccentricity = eigen_value[0]/eigen_value[1]
        l = [mean_area, r,b,g,eigen_value[0],eigen_value[1], eccentricity]
        ftrain.append(np.array(l))
    ftest = []
    for gi in range(len(xctest)):
        gcolor = xctest[gi]
        ggray = xgtest[gi]
        h, w = ggray.shape
        area = np.sum(np.sum([[1.0 for j in range(w) if ggray[i,j]] for i in range(h)]))
        mean_area = area / (h * w)
        r, b, g = np.sum([gcolor[i, j] for j in range(gcolor.shape[1]) for i in range(gcolor.shape[0])], axis=0) / (area*256)
        _, _, eigen_value = pca(ggray)
        eccentricity = eigen_value[0] / eigen_value[1]
        l = [mean_area, r,b,g,eigen_value[0],eigen_value[1], eccentricity]
        ftest.append(l)

    # MLP
    print "Trainning linear MLP..."
    model = train(np.array(ftrain), np.array(y_train), 'weights.pkl')
    score = model.evaluate(np.array(ftest), np.array(y_test))
    print('cnn Test loss:', score[0])
    print('cnn Test accuracy:', score[1])