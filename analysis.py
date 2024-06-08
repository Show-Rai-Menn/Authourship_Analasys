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
def token_frequency(content, token_num):
    print('start token search')
    print(f'token_num = {token_num}')
    doc=nlp(content)


    word_freq = Counter(token.text.lower() for token in doc if token.is_alpha)

    top_words=word_freq.most_common(token_num)
    
    return top_words
    #返り値はtokenのlist(string)






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
        

    