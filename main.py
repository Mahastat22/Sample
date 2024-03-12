"""
import spacy
import re
nlp = spacy.load("en_core_web_sm")
#with json data
#nodes function - a function that takes json text input and return nodes of the given text
nodes = set()
def keyword_extraction(texts):
  doc = nlp(texts)
  for ent in doc.ents:
    nodes.add(ent.text)
  for token in doc:
    if token.dep_ in ("nsubj", "nsubjpass", "dobj", "pobj", "attr"):
      head = token.head.text
      dep = token.dep_
      child = token.text
      nodes.add(head)
      nodes.add(child)
      pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, nodes)) + r')\b', re.IGNORECASE)
      def underline_match(match):
        return f"_{match.group(0)}_"
      result = pattern.sub(underline_match, texts)
      underlined_words = re.findall(r'_([^_]+)_', result)
      output = ' '.join(underlined_words)
  return output
from flask import Flask, request, jsonify
app= Flask(__name__)
@app.route('/key', methods=['POST'])
def keyword():
    try:
        data = request.get_json()
        texts = data['text']
        result = {'extracted': keyword_extraction(texts)}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
"""
if __name__ == '__main__':
    app.run(debug=True)


