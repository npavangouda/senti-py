#!flask/bin/python
import pdb
import os
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from textblob import TextBlob
from flask_cors import CORS, cross_origin
from textblob.classifiers import NaiveBayesClassifier
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

cl = None

@app.route('/senti/api/textblob', methods=['POST'])
def analyze_conv():
    print(request.json)
    if not request.json:
        abort(400)
    
    sampleText = request.json['text']
    
    testimonial = TextBlob(sampleText)
    print(testimonial.sentiment.polarity)
    
    response = createSentiResponse(sampleText, testimonial.sentiment.polarity, 0.5, 0.0)
    
    return jsonify({'sentiment': response}), 201

@app.route('/senti/api/vader', methods=['POST'])     
def analyze_text_vader():
    print(request.json)
    if not request.json:
        abort(400)
    
    sampleText = request.json['text']  
    
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sampleText)
    print(vs)
    
    response = createSentiResponse(sampleText, vs['compound'], 0.1, -0.1)
    
    return jsonify({'sentiment': response})
     
    

@app.route('/senti/api/bayes/train', methods=['GET'])
def text_senti_train():
    train_nbc()

@app.route('/senti/api/bayes', methods=['POST'])
def analyze_text_senti():
    print(request.json)
    if not request.json:
        abort(400)
      
    convTemp = {
        'text': request.json['text'],
        'polarity': 0,
        'senti': ''
    }
    
    output = classify(convTemp['text'])
    return jsonify({'sentiment': output})

def train_nbc():
        cl = None
        train = [
                 ('I love this sandwich.', 'pos'),
                 ('this is an amazing place!', 'pos'),
                 ('I feel very good about these beers.', 'pos'),
                 ('this is my best work.', 'pos'),
                 ("what an awesome view", 'pos'),
                 ('I do not like this restaurant', 'neg'),
                 ('I am tired of this stuff.', 'neg'),
                 ("I can't deal with this", 'neg'),
                 ('he is my sworn enemy!', 'neg'),
                 ('my boss is horrible.', 'neg')
                ]
        cl = NaiveBayesClassifier(train)
 
def classify(text):
    output = cl.classify(text)
    print(output)    
    return output

def createSentiResponse(inputText, polarity, min, max):
        
    sentiResp = {
        'text': inputText,
        'polarity': 0,
        'senti': ''
    }
    
    sentiResp['polarity'] = polarity
    
    if polarity > min :
        sentiResp['senti'] = 'P'
    elif polarity < max:
        sentiResp['senti'] = 'N'
    else:
        sentiResp['senti'] = 'U'
    
    return sentiResp

    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)
