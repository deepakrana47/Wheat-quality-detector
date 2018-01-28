from  segment_formation_1 import segment_image
from PCA import pca
import numpy as np, keras, cv2

if __name__ == "__main__":
    imgFile =  raw_input("Enter the file(wheat image) location to dectect : ")
    # imgFile = '/media/zero/41FF48D81730BD9B/kisannetwork/IMG_20161016_123346545.jpeg'

    print "Segmentation in process..."
    segments, segLocation= segment_image(imgFile)
    print "Segmentation in Complete."


    features = {}
    print "Feature extraction in process..."
    for gi in segments:
        gcolor = segments[gi]
        h, w, _ = gcolor.shape
        ggray = np.array([[gcolor[i,j,2] for j in range(w)] for i in range(h)], dtype=np.uint8)
        area = np.sum(np.sum([[1.0 for j in range(w) if ggray[i, j]] for i in range(h)]))
        mean_area = area / (h * w)
        r, b, g = np.sum([gcolor[i, j] for j in range(w) for i in range(h)], axis=0) / (area * 256)
        _, _, eigen_value = pca(ggray)
        eccentricity = eigen_value[0] / eigen_value[1]
        l = [mean_area, r, b, g, eigen_value[0], eigen_value[1], eccentricity]
        features[gi] = np.array(l)
    print "Featur extraction in complete."

    model = keras.models.load_model('weights.pkl')
    out = {}
    for i in features:
        out[i] = model.predict(np.array([features[i]]))

    img = cv2.imread(imgFile, cv2.IMREAD_COLOR)
    good = not_good = 0
    for i in out:
        s = segLocation[i]
        if np.argmax(out[i][0]) == 0:
            good += 1
            rect = cv2.rectangle(img, (s[2], s[0]), (s[3], s[1]), (255, 0, 0), 1)
        else:
            not_good+=1
            rect = cv2.rectangle(img, (s[2], s[0]), (s[3], s[1]), (0, 0, 255), 3)
    print "Number of good grain :", good
    print "Number Not good grain or imputity:", not_good
    cv2.imwrite("result_image.jpg", img)


    # to display image
    cv2.imshow("result_image.jpg", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

