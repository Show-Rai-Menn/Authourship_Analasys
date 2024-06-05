import os
import spacy
import re
from datetime import datetime
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Load SpaCy English model
nlp = spacy.load('en_core_web_sm')

def load_files_from_directory(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    data = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_content = read_file(file_path)
            if file_content:
                data.append(file_content)
    return data

def read_file(file_path):
    encodings = ['utf-8', 'shift_jis', 'iso-8859-1', 'cp932']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    print(f"Could not read file {file_path} with available encodings.")
    return None

def search_word_token(texts, keyword, context_size=5):
    results = []
    for text in texts:
        doc = nlp(text)
        for token in doc:
            if token.text.lower() == keyword.lower():
                start = max(0, token.i - context_size)
                end = min(len(doc), token.i + context_size + 1)
                context = doc[start:end]
                context_tokens = [tok.text_with_ws for tok in context]
                keyword_index = token.i - start
                context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                result = "".join(context_tokens)
                results.append(result)
    return results

def search_lemma(texts, keyword, context_size=5):
    results = []
    for text in texts:
        doc = nlp(text)
        for token in doc:
            if token.lemma_.lower() == keyword.lower():
                start = max(0, token.i - context_size)
                end = min(len(doc), token.i + context_size + 1)
                context = doc[start:end]
                context_tokens = [tok.text_with_ws for tok in context]
                keyword_index = token.i - start
                context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                result = "".join(context_tokens)
                results.append(result)
    return results

def search_pos(texts, keyword, context_size=5):
    results = []
    for text in texts:
        doc = nlp(text)
        for token in doc:
            if token.pos_ == keyword:
                start = max(0, token.i - context_size)
                end = min(len(doc), token.i + context_size + 1)
                context = doc[start:end]
                context_tokens = [tok.text_with_ws for tok in context]
                keyword_index = token.i - start
                context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                result = "".join(context_tokens)
                results.append(result)
    return results

def search_ngram(texts, keyword, n, context_size=5):
    results = []
    for text in texts:
        doc = nlp(text)
        tokens = [token.text for token in doc]
        for i in range(len(tokens) - n + 1):
            ngram = " ".join(tokens[i:i + n])
            if keyword.lower() in ngram.lower():
                start = max(0, i - context_size)
                end = min(len(tokens), i + n + context_size)
                context_tokens = tokens[start:end]
                keyword_index = context_tokens.index(tokens[i])
                context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                result = " ".join(context_tokens)
                results.append(result)
    return results

def search_regex(texts, pattern, context_size=5):
    results = []
    regex = re.compile(pattern, re.IGNORECASE)
    for text in texts:
        matches = regex.finditer(text)
        for match in matches:
            start = max(0, match.start() - context_size * 6)  # 1単語あたりの平均文字数を6と仮定
            end = min(len(text), match.end() + context_size * 6)
            context = text[start:end]
            highlighted = re.sub(pattern, f"<span class='highlight'>{match.group()}</span>", context, flags=re.IGNORECASE)
            results.append(highlighted)
    return results

@app.route('/')
def index():
    return render_template('exploratory.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    search_type = data['searchType']
    search_term = data['searchTerm']
    directory = './AA dataset'
    try:
        texts = load_files_from_directory(directory)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 400

    context_size = 5

    if search_type == 'wordToken':
        results = search_word_token(texts, search_term, context_size)
    elif search_type == 'lemma':
        results = search_lemma(texts, search_term, context_size)
    elif search_type == 'pos':
        results = search_pos(texts, search_term, context_size)
    elif search_type == 'ngram':
        n = 3  # Default value for n-gram, can be adjusted as needed
        results = search_ngram(texts, search_term, n, context_size)
    elif search_type == 'regex':
        results = search_regex(texts, search_term, context_size)
    else:
        results = []

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
