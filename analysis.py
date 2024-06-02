import spacy
from collections import Counter, defaultdict
import os
import heapq



nlp = spacy.load("en_core_web_sm")


text = """
Your text goes here. This is a sample text to demonstrate the frequency of words.
You can replace this text with any other text you want to analyze.
"""

#token_numで何単語出力するのかを決める
def token_frequency(file_path, token_num):
    try:
        with open(file_path, 'r') as f:
            content=f.read()
        

        doc=nlp(content)

        words=(token.text.lower() for token in doc if not token.is_punct)

        word_freq = Counter(words)

        top_words=heapq.nlargest(token_num, word_freq.items(), key=lambda x:x[1])

        return top_words
    #返り値はtokenのlist(string)
    except FileNotFoundError:
        print("Error file not found ", file_path)
        return
    except :
        print("Error")
        return

def load_files(file_path):

    try:
        with open(file_path, 'r') as file:  # 念の為utf-8で読み込む。
            data=file.read()
        
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return data

def token_search(keyword, filepath, context_size=5):
    ### ワード検索の関数 ###
    text=load_files(filepath)
    results = []
    
    doc = nlp(text) # docはトークン化された単語などを含むドキュメントオブジェクト
    for token in doc:
        if token.text.lower() == keyword.lower(): #　小文字で比較　→　大文字小文字区別無くす
            start = max(0, token.i - context_size)  # 出力開始位置を求める # token.iはトークンのインデックス
            end = min(len(doc), token.i + context_size + 1)  #出力の終わりの位置　
                
            context = doc[start:end]  #キーワード含めて取得
            context_tokens = [tok.text_with_ws for tok in context]
            
                
                # キーワードを赤色にする
            keyword_index = token.i - start
            context_tokens[keyword_index] = f"<span style='color:red;'>{context_tokens[keyword_index]}</span>"#直接htmlを書いておく
                
            result = "".join(context_tokens)  # join関数を使用してリスト内の文字列を結合する
            results.append(result)
    return results


def K_and_K(filenames, contents):
    
    counter=create_Counter(contents, filenames)
    
    newcounter=sort_counter(counter)
    
    return newcounter
    






def create_Counter(contents, filenames):
    
    counter = defaultdict(Counter)
    for content, filename in zip(contents, filenames):
        print(type(content))
        print(filename)
        doc = nlp(content)  # contentを文字列として渡す
        seen_tokens = set()
        for token in doc:
            if token.text.lower().isalpha():
                token_text=token.text.lower()
                counter[token_text][filename]+=1
                if token_text not in seen_tokens:
                    counter[token_text]['sum'] += 1
                    seen_tokens.add(token_text)
            
    return counter

def sort_counter(counter):
    sort_item= sorted(counter.items(), key=lambda item: item[1]['sum'], reverse=True)

    sorted_item=defaultdict(Counter, sort_item)
    return sorted_item
        

    