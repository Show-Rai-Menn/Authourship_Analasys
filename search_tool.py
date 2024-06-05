import os
import spacy
import re
from datetime import datetime

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

def generate_filename(term):
    case_number = "001"  # This should be generated or passed as an argument based on the actual use case
    now = datetime.now().strftime("%Y%m%d-%H%M")
    initials = "MY"  # Replace with actual initials as needed
    return f"{case_number}-{now}-{initials}-{term}.txt"

def save_results(results, term):
    filename = generate_filename(term)
    with open(filename, 'w', encoding='utf-8') as file:
        for result in results:
            file.write(result + "\n")
    print(f"Results saved to {filename}")

def main():
    directory = './AA dataset'  # Replace with your directory
    search_type = input("Enter the type of search (wordToken, lemma, pos, ngram, regex): ").strip()
    search_term = input("Enter the search term or pattern: ").strip()
    
    try:
        texts = load_files_from_directory(directory)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    context_size = 5  # Adjust as needed

    if search_type == 'wordToken':
        results = search_word_token(texts, search_term, context_size)
    elif search_type == 'lemma':
        results = search_lemma(texts, search_term, context_size)
    elif search_type == 'pos':
        results = search_pos(texts, search_term, context_size)
    elif search_type == 'ngram':
        n = int(input("Enter the value of n for n-gram search: "))
        results = search_ngram(texts, search_term, n, context_size)
    elif search_type == 'regex':
        results = search_regex(texts, search_term, context_size)
    else:
        print("Invalid search type.")
        return

    save_results(results, search_term)
    print("Search results:")
    for result in results:
        print(result)

if __name__ == '__main__':
    main()
