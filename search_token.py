import spacy
from collections import Counter
import os




nlp = spacy.load("en_core_web_sm")


text = """
Your text goes here. This is a sample text to demonstrate the frequency of words.
You can replace this text with any other text you want to analyze.
"""

#token_numで何単語出力するのかを決める
def search_token(file_path, token_num):
    try:
        with open(file_path, 'r') as f:
            content=f.read()
        

        doc=nlp(content)

        words=[token.text.lower() for token in doc if not token.is_punct]

        word_freq = Counter(words)

        top_words=word_freq.most_common(token_num)

        return top_words
    #返り値はtokenのlist(string)
    except FileNotFoundError:
        print("Error file not found ", file_path)
        return
    except :
        print("Error")
        return


