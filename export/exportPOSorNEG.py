import pickle
import sys
import os
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def usage():
    print("Usage:")
    print("python %s <data_dir>" % sys.argv[0])

if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    data_dir = sys.argv[1]
    classes = ['pos', 'neg']

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    iterator = 0
    for curr_class in classes:
        dirname = os.path.join(data_dir, curr_class)
        for fname in os.listdir(dirname):
            if iterator > 900:
                iterator=0 
                break
            iterator = iterator + 1
            with open(os.path.join(dirname, fname), 'r') as f:
                content = f.read()
                if iterator > 900:
                    test_data.append(content)
                    test_labels.append(curr_class)
                else:
                    train_data.append(content)
                    train_labels.append(curr_class)

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.85,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)

    # Perform classification with SVM, kernel=rbf
    # classifier_rbf = svm.SVC()
    # t0 = time.time()
    # classifier_rbf.fit(train_vectors, train_labels)
    # t1 = time.time()

   


    # t2 = time.time()
    # time_rbf_train = t1-t0
    # time_rbf_predict = t2-t1

    # Perform classification with SVM, kernel=linear

    with open('vectorizerPOSITIVE_NEGATIVE.pk', 'wb') as fin:
        pickle.dump(vectorizer, fin)