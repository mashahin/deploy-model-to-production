from flask import jsonify, request, Flask
from sklearn.externals import joblib

models = joblib.load('models')
app = Flask(__name__)


@app.route('/', methods=['POST'])
def predict():
    text = request.form.get('text')
    results = {}
    for name, clf in models.iteritems():
        results[name] = clf.predict([text])[0]
    return jsonify(results)


if __name__ == '__main__':
    app.run()
