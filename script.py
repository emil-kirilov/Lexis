#http://gizmodo.com/the-best-worst-product-reviews-on-amazon-1648733527 - test reviews amazon
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
    classes = ['anger', 'fear', 'sadness', 'surprise', 'happiness', 'neutral', 'disgust']

    # Read the data
    train_data = []
    train_labels = []
    test_data = []
    test_labels = []
    iterator = 0
    for curr_class in classes:
        dirname = os.path.join(data_dir, curr_class)
        for fname in os.listdir(dirname):
            if iterator > 5000:
                iterator=0 
                break
            iterator = iterator + 1
            with open(os.path.join(dirname, fname), 'r') as f:
                content = f.read()
                if iterator > 4000:
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
    test_vectors = vectorizer.transform(test_data)

    our_test = vectorizer.transform(["I hate it. This is murder. This is soo bad."]) 

    # Perform classification with SVM, kernel=rbf
    # classifier_rbf = svm.SVC()
    # t0 = time.time()
    # classifier_rbf.fit(train_vectors, train_labels)
    # t1 = time.time()

   


    # t2 = time.time()
    # time_rbf_train = t1-t0
    # time_rbf_predict = t2-t1

    # Perform classification with SVM, kernel=linear
    #removed ", decision_function_shape = 'ovo'"
    classifier_linear = svm.SVC(kernel='linear', C=10, probability=True)
    t0 = time.time()
    classifier_linear.fit(train_vectors, train_labels)
    t1 = time.time()
    while True:
        var = raw_input("Please enter something: ")
        our_test = vectorizer.transform([var])
        prediction_rbf = classifier_linear.predict(our_test)
        priediction_proba = classifier_linear.predict_proba(our_test)
        print(zip(classifier_linear.classes_, priediction_proba[0])) #shows all propabilities
        print(prediction_rbf) #shows determined label
    
    # exit()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1-t0
    time_linear_predict = t2-t1

    # Perform classification with SVM, kernel=linear
    # classifier_liblinear = svm.LinearSVC()
    # t0 = time.time()
    # classifier_liblinear.fit(train_vectors, train_labels)
    # t1 = time.time()
    # prediction_liblinear = classifier_liblinear.predict(test_vectors)
    # t2 = time.time()
    # time_liblinear_train = t1-t0
    # time_liblinear_predict = t2-t1

    # Print results in a nice table
    # print("Results for SVC(kernel=rbf)")
    # print("Training time: %fs; Prediction time: %fs" % (time_rbf_train, time_rbf_predict))
    # print(classification_report(test_labels, prediction_rbf))
    print("Results for SVC(kernel=linear)")
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    print(classification_report(test_labels, prediction_linear))
    # print("Results for LinearSVC()")
    # print("Training time: %fs; Prediction time: %fs" % (time_liblinear_train, time_liblinear_predict))
    # print(classification_report(test_labels, prediction_liblinear))