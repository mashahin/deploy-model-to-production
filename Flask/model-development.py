from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.svm import LinearSVC

# code to load training data into X_train, y_train, split train/test set

vec = HashingVectorizer()
svc = LinearSVC()
clf = make_pipeline(vec, svc)
svc.fit(X_train, y_train)

joblib.dump({'class1': clf}, 'models', compress=9)
