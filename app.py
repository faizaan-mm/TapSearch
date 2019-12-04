from flask import *
import string


app = Flask(__name__)


indexed_docs = {}
inputs = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/indextext', methods=['POST'])
def indextext():
	inputs['text'] = request.form["text"].lower()
	inputs['word'] = request.form["word"].lower()
	table = str.maketrans(dict.fromkeys(string.punctuation))
	inputs['text'] = inputs['text'].translate(table)
	paragraphs = inputs['text'].split('\r\n\r\n\r\n')
	for i in range(0,len(paragraphs)):
		indexed_docs[i+1]=paragraphs[i].split()
	return redirect('/')


@app.route('/cleartext', methods=['POST'])
def cleartext():
	indexed_docs.clear()
	return redirect('/')


@app.route('/search', methods=['POST'])
def search():
	word_frequency = {}
	for i in range(1,len(indexed_docs)+1):
		for word in indexed_docs[i]:
			if inputs['word'] == word:
				if i in word_frequency.keys():
					word_frequency[i] += 1
				else:
					word_frequency[i] = 1
	print(word_frequency)
	word_frequency = sorted(word_frequency.items(), key=lambda kv: kv[1], reverse=True)
	word_frequency = word_frequency[:10]
	print(word_frequency)
	return render_template('results.html', result = word_frequency)


if __name__ == '__main__':
	app.run(threaded=True, port=5000, debug=False)
