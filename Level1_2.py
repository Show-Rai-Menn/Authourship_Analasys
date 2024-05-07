import os
import re
from datetime import datetime
import spacy

nlp = spacy.load('en_core_web_sm')

def load_files(file_paths):
    data = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data.append(file.read())
    return data

def search_texts(texts, search_type, keyword):
    results = []
    for text in texts:
        doc = nlp(text)
        for token in doc:
            if ((search_type == 'word_token' and token.text == keyword) or
                (search_type == 'lemma' and token.lemma_ == keyword) or
                (search_type == 'POS' and token.pos_ == keyword)):
                start = max(0, token.i - 5)
                end = min(len(doc), token.i + 5)
                context = doc[start:end]
                result = " ".join([tok.text_with_ws for tok in context])
                highlight = result.replace(keyword, f"\033[1;31m{keyword}\033[0m")  # キーワードを赤色で表示
                results.append(highlight)
        if search_type == 'regex':
            matches = re.finditer(keyword, text)
            for match in matches:
                start = max(0, match.start() - 10)
                end = min(len(text), match.end() + 10)
                results.append(text[start:end].replace(keyword, f"\033[1;31m{keyword}\033[0m"))
    return results

def save_results(results, case_number, initials, term):
    date_time = datetime.now().strftime("%Y%m%d-%H%M")
    file_name = f"{case_number}-{date_time}-{initials}-{term}.txt"
    with open(file_name, 'w') as file:
        for result in results:
            file.write(result + '\n')

def main():
    file_paths = ['file1.txt', 'file2.txt']
    search_type = 'word_token'  # 検索タイプはユーザーの入力に基づいて変更可能
    keyword = 'banana'
    case_number = '001'
    initials = 'XYZ'

    texts = load_files(file_paths)
    results = search_texts(texts, search_type, keyword)
    save_results(results, case_number, initials, keyword)

if __name__ == "__main__":
    main()
