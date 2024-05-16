import os
import spacy

# Load SpaCy English model
nlp = spacy.load('en_core_web_sm')

def load_files(file_paths):
    data = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # 念の為utf-8で読み込む。
                data.append(file.read())
        except FileNotFoundError:
            print(f"File not found: {file_path}")
    return data

def search_word_token(texts, keyword, context_size=5):
    ### ワード検索の関数 ###
    results = []
    for text in texts:
        doc = nlp(text) # docはトークン化された単語などを含むドキュメントオブジェクト
        for token in doc:
            if token.text.lower() == keyword.lower(): #　小文字で比較　→　大文字小文字区別無くす
                start = max(0, token.i - context_size)  # 出力開始位置を求める # token.iはトークンのインデックス
                end = min(len(doc), token.i + context_size + 1)  #出力の終わりの位置　
                
                context = doc[start:end]  #キーワード含めて取得
                context_tokens = [tok.text_with_ws for tok in context]
                
                # キーワードを赤色にする
                keyword_index = token.i - start
                context_tokens[keyword_index] = f"\033[1;31m{context_tokens[keyword_index]}\033[0m"  # 赤色で表示　（GUI実装したら消す）
                
                result = "".join(context_tokens)  # join関数を使用してリスト内の文字列を結合する
                results.append(result)
    return results

def main():
    # 今回はファイルをパスで指定して、リストに格納
    file_paths = ['/Users/mizut/Authorship/file1.txt', '/Users/mizut/Authorship/file2.txt']  # 検索したいテキスト（1つ以上）
    search_type = 'word_token'  #　最初はワードトークンごとに検索
    keyword = 'banana'  # 検索したいワードトークン
    context_size = 5  # 出力の時キーワードの左右それぞれに表示する数

    texts = load_files(file_paths)
    if search_type == 'word_token':
        results = search_word_token(texts, keyword, context_size)
        return results

if __name__ == "__main__":
    search_results = main()
    for result in search_results:
        print(result)


