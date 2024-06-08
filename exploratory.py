import os
import spacy
import re
from datetime import datetime
from collections import Counter




# Load SpaCy English model
nlp = spacy.load('en_core_web_sm')


def search_word_token(Qfilenames, Qcontents, Kfilenames, Kcontents, keyword, context_size=10):
    print('start token search')
    Qresults={}
    Kresults={}
    if Qcontents is []:
        Qresults={}
    else:
        for filename, content in zip(Qfilenames, Qcontents):
            doc=nlp(content)
            Qresults[filename]=[]
            for token in doc:
                if token.text.lower() == keyword.lower():
                    start = max(0, token.i - context_size)
                    end = min(len(doc), token.i + context_size + 1)
                    context = doc[start:end]
                    context_tokens = [tok.text_with_ws for tok in context]
                    keyword_index = token.i - start
                    context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                    result = "".join(context_tokens)
                    Qresults[filename].append(result)

    
    if Kcontents is []:
        Kresults={}
    else:
        for filename, content in zip(Kfilenames, Kcontents):
            doc=nlp(content)
            Kresults[filename]=[]
            for token in doc:
                if token.text.lower() == keyword.lower():
                    start = max(0, token.i - context_size)
                    end = min(len(doc), token.i + context_size + 1)
                    context = doc[start:end]
                    context_tokens = [tok.text_with_ws for tok in context]
                    keyword_index = token.i - start
                    context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                    result = "".join(context_tokens)
                    Kresults[filename].append(result)
 
    return Qresults, Kresults

def search_lemma(Qfilenames, Qcontents, Kfilenames, Kcontents, keyword, context_size=10):


    print('start lema search')
    Qresults={}
    Kresults={}
    if Qcontents is []:
        Qresults={}
    else:
        for filename, content in zip(Qfilenames, Qcontents):
            doc=nlp(content)
            Qresults[filename]=[]
            for token in doc:
                if token.lemma_.lower() == keyword.lower():
                    start = max(0, token.i - context_size)
                    end = min(len(doc), token.i + context_size + 1)
                    context = doc[start:end]
                    context_tokens = [tok.text_with_ws for tok in context]
                    keyword_index = token.i - start
                    context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                    result = "".join(context_tokens)
                    Qresults[filename].append(result)

    
    if Kcontents is []:
        Kresults=[]
    else:
        for filename, content in zip(Kfilenames, Kcontents):
            doc=nlp(content)
            Kresults[filename]=[]
            for token in doc:
                if token.lemma_.lower() == keyword.lower():
                    start = max(0, token.i - context_size)
                    end = min(len(doc), token.i + context_size + 1)
                    context = doc[start:end]
                    context_tokens = [tok.text_with_ws for tok in context]
                    keyword_index = token.i - start
                    context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                    result = "".join(context_tokens)
                    Kresults[filename].append(result)


    return Qresults, Kresults

def search_pos(Qfilenames, Qcontents, Kfilenames, Kcontents, keyword, context_size=10):



    print('start pos search')
    Qresults={}
    Kresults={}
    if Qcontents is []:
        Qresults={}
    else:
        for filename, content in zip(Qfilenames, Qcontents):
            doc=nlp(content)
            Qresults[filename]=[]
            for token in doc:
                if token.pos_ == keyword:
                    start = max(0, token.i - context_size)
                    end = min(len(doc), token.i + context_size + 1)
                    context = doc[start:end]
                    context_tokens = [tok.text_with_ws for tok in context]
                    keyword_index = token.i - start
                    context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                    result = "".join(context_tokens)
                    Qresults[filename].append(result)

    
    if Kcontents is []:
        Kresults=[]
    else:
        for filename, content in zip(Kfilenames, Kcontents):
            doc=nlp(content)
            Kresults[filename]=[]
            for token in doc:
                if token.pos_ == keyword:
                    start = max(0, token.i - context_size)
                    end = min(len(doc), token.i + context_size + 1)
                    context = doc[start:end]
                    context_tokens = [tok.text_with_ws for tok in context]
                    keyword_index = token.i - start
                    context_tokens[keyword_index] = f"<span class='highlight'>{context_tokens[keyword_index]}</span>"
                    result = "".join(context_tokens)
                    Kresults[filename].append(result)

    return Qresults, Kresults

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


