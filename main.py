
from transformers import pipeline
from transformers import AutoModelForSequenceClassification

pipe = pipeline(model="facebook/bart-large-mnli")
def tag(texts):
    output = pipe(texts, candidate_labels=['Upgrades','Partnerships','Team updates','Events','Market insights','ICO announcements','White Paper release','ICO updates', 'Others',
'NFT release','Partnership with NFT artists','Platform updates','Community discussion / AMAs','Airdrops','Contests / Give-aways','Regulatory updates','Security updates'
],)
    return output

from flask import Flask, request, jsonify
application = Flask(__name__)
app=application
@app.route('/tagging', methods=['POST'])
def tags():
    try:
        data = request.get_json()
        texts = data['text']
        result = tag(texts)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
