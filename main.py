from matplotlib import image
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering


def main():
    pic_pixels, pic_labels = get_data()
    k_means = KMeans(n_clusters=40, init='random').fit(pic_pixels)
    dbscan = DBSCAN(eps=2300, min_samples=4).fit(pic_pixels)
    agglomerativeGA = AgglomerativeClustering(n_clusters=40, linkage='average').fit(pic_pixels)
    agglomerativeCL = AgglomerativeClustering(n_clusters=40, linkage='complete').fit(pic_pixels)
    agglomerativeSL = AgglomerativeClustering(n_clusters=40, linkage='single').fit(pic_pixels)

    print("K-Means Rand Index:")
    print("%.2f" % randIndex(pic_labels, k_means.labels_))
    print("DBSCAN Rand Index:")
    print("%.2f" % randIndex(pic_labels, dbscan.labels_))
    print("Agglomerative single link Rand Index:")
    print("%.2f" % randIndex(pic_labels, agglomerativeSL.labels_))
    print("Agglomerative complete link Rand Index:")
    print("%.2f" % randIndex(pic_labels, agglomerativeCL.labels_))
    print("Agglomerative average link Rand Index:")
    print("%.2f" % randIndex(pic_labels, agglomerativeGA.labels_))


def randIndex(pic_labels, generated_labels):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(1, 400):
        for j in range(i+1, 400):
            if pic_labels[i] == pic_labels[j]: #same clusters
                if generated_labels[i] == generated_labels[j]: #same label
                    tp += 1
                else:
                    fp += 1
            else:
                if generated_labels[i] == generated_labels[j]:
                    fn += 1
                else:
                    tn += 1
    ri = (tp + tn)/(tp + fp + fn + tn)
    return ri


def get_data():
    pic_pixels = list()
    pic_labels = list()
    person_num = 1
    root = 'data/'
    for picNum in range(1,401):
        label = str(picNum) + "_" + str(person_num) #pic labels
        pic_labels.append(person_num-1)
        if picNum %10 == 0:
            person_num += 1
        data_image = image.imread(root + label + ".jpg")
        #pic size from 70*80 to 1*5600
        flat_pic = data_image.flatten(order='C')
        pic_pixels.append(flat_pic)
    return pic_pixels, pic_labels


if __name__ == "__main__":
    main()
