#!flask/bin/python
from flask import Flask, jsonify
import os
from flask import abort
from flask import make_response
from flask import request
from textblob import TextBlob
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)

conversations = [
    {
        'id': 1,
        'text': u'It is nice working here.',
        'polarity': 2, 
        'senti': 'P'
    }
]

@app.route('/senti/api/conversations', methods=['GET'])
def get_conversations():
    return jsonify({'conversations': conversations})
    
    
@app.route('/senti/api/conversation', methods=['POST'])
def analyze_conv():
    print(request.json)
    if not request.json:
        abort(400)
    
    convTemp = {
        'id': conversations[-1]['id'] + 1,
        'text': request.json['text'],
        'polarity': 0,
        'senti': ''
    }
    
    testimonial = TextBlob(convTemp['text'])
    print(testimonial.sentiment.polarity)
    convTemp['polarity'] = testimonial.sentiment.polarity
    
    if testimonial.sentiment.polarity > 0.5 :
        convTemp['senti'] = 'P'
    elif testimonial.sentiment.polarity < 0.0:
        convTemp['senti'] = 'N'
    else:
        convTemp['senti'] = 'U'
        
    
    # conversations.append(convTemp)
    return jsonify({'conv': convTemp}), 201
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)
