import codecs
import json
from fakenews_model import predict_article
from fakenews_model import train_model
from scraping_train import scrapTrain
from nlp import tokenize, pos_tag, rm_stop_words, bag_of_words, lemmatization, stemming, tfidf
from db import scraping_collection_train, scraping_collection_predectid
from textblob import TextBlob
import re
from json import JSONEncoder
import threading
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_cors import CORS
from schema import schema
from datetime import datetime
from flask_graphql import GraphQLView
app = Flask(__name__)

CORS(app)


@app.route('/process_text', methods=['POST'])
def process_text():
    _json = request.get_json(force=True)
    if not "method" in _json or not "text" in _json:
        return not_found()
    text = _json['text']
    method = _json['method']
    result = None

    if method == "tokenization":
        result = tokenize(text)
    elif method == "pos_tag":
        result = pos_tag(tokenize(text))
    elif method == "rm_stop_words":
        result = rm_stop_words(text)
    elif method == "lemmatization":
        result = lemmatization(text)
    elif method == "tfidf":
        result = tfidf(text)
    elif method == "stemming":
        result = stemming(text)
    elif method == "bag_of_words":  # expecting an array of texts
        result = bag_of_words(text)
    response = jsonify({"data": result})
    return response


@app.route('/emotion', methods=['POST'])
def emotion():
    _json = request.get_json(force=True)
    if not "text" in _json:
        return not_found()
    text = _json['text']
    s = TextBlob(text)
    emotion = s.sentiment.polarity
    if emotion == 0:
        res = "neutral"
    elif emotion > 0:
        res = "positive"
    else:
        res = "negative"
    response = jsonify({"success": True, "data": res})

    return response

@app.route('/scrap_train', methods=['POST'])
def loadscrap():
    _json = request.get_json(force=True)
    if not "number" in _json:
        return not_found()
    number = _json['number']
    rows = scrapTrain(number)
    for row in rows:
        scraping_collection_train.insert(
                {'link':row['link'], 'text': row['text'],'source': row['source'], 'label': row['label']})
    response = jsonify({"success": True, "data": "scrapted"})
    return response

@app.route('/scrap_predict', methods=['POST'])
def add():
    _json = request.get_json(force=True)
    if not "number" in _json:
        return not_found()
    number = _json['number']
    rows = scrapTrain(number)
    for row in rows:
        scraping_collection_predectid.insert({
            'link':row['link'],
            'text': row['text'],
            'source': row['source'],
            'date': datetime.now(),
            'prediction': predict_article(row['text'])
        })

    response = jsonify({"success": True, "data": "scrapted"})
    return response

@app.route('/data', methods=['GET'])
def get_all_data():
    data = scraping_collection_predectid.find()
    resp = dumps(data)
    return resp


@app.route('/predict/fakenews', methods=['POST'])
def predict():
    _json = request.get_json(force=True)
    if not "article" in _json:
        return not_found()
    article = _json['article']

    return jsonify({"isFake":  predict_article(article)})


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
