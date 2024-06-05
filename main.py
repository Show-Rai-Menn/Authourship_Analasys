from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import os
from werkzeug.utils import secure_filename
import db
import analysis
from concurrent.futures import ThreadPoolExecutor, as_completed
import exploratory

app = Flask(__name__)

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/file')
def file():
    
    Q_file=db.search_allQ()
    K_files=db.search_allK()
    
    return render_template('file.html', Q_file=Q_file, K_files=K_files)

@app.route('/exploratory')
def exploratory():
    Q_file=db.search_allQ()
    K_files=db.search_allK()
    return render_template('exploratory.html', Q_file=Q_file, K_files=K_files)

@app.route('/explonatory/search', methods=['POST'])
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



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return render_template('file.html', message='No file part')
    
    files = request.files.getlist('files')
    if not files:
        return render_template('file.html', message='No selected file')
    
    kind=request.form.get('kind')
    
    for file in files:
        if file.filename == '':
            return render_template('file.html', message='No selected file')#ファイル選択画面を開いたが何も選択していない場合
        
        content = file.read().decode('shift_jis')  # テキストファイルの場合
       
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            if kind=="upload as Q":
                db.upload(filename, 'Q', content)
            elif kind=="upload as K":
                db.upload(filename, 'K', content)
            

        else:
            return render_template('file.html', message='file extension is wrong')#拡張子が違うとき

    return render_template('file.html', message='file upload successfully and please reload')#正常なとき


@app.route('/K_and_K')
def K_and_K():
    K_files=db.search_allK()
    
    return render_template('K_and_K.html',  K_files=K_files)
    
@app.route('/K_and_K/result', methods=['POST'])
def Kresult():
    Kfilename=request.form.getlist('K')
    null, Kfiles=db.get_content(None, Kfilename)
    
    result=analysis.K_and_K(Kfilename, Kfiles)
    return render_template('K_and_K_result.html', result=result)

@app.route('/search/file')
def search():
    search_query = request.args.get('query', '')
    file_name=db.search(search_query)
    return jsonify([name[0] for name in file_name])

@app.route('/search')
def search_file():
    return render_template('search.html')



@app.route('/delete', methods=['POST'])
def delete():
    filename=request.form['filename']
    filepath = os.path.join('uploads', filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        db.delete_file(filename)
        print('File successfully deleted.')

    else :
        print('File not found.')

    return redirect(url_for('index'))

@app.route('/update')
def update():
    return render_template('file.html', method='Update')

@app.route('/select')
def select_file():
    filename=db.search_all()
    
    return render_template('select.html', namelist=filename)

@app.route('/token', methods=['POST'])
def token_frequency():#ここでは選択されたファイルを受け取ってtoken frequencyの処理をしている
    try:
        print("success access /token")
        selected=request.form.getlist("option")
        counter=int(request.form.get('counter'))
        token_num = counter * 20

        # 選択されたファイルのパスを生成
        file_paths = [os.path.join("uploads", filename) for filename in selected]
        
        # ファイルを処理する関数
        def process_file(filepath):
            tokenlist = analysis.token_frequency(filepath, token_num)
            if tokenlist is None:
                tokenlist = []  # listの初期化
                print("tokenlist is none")
            filename = os.path.basename(filepath)
            return filename, tokenlist
        
        filelist = []
        
        # ThreadPoolExecutorを使用して非同期にファイルを処理
        with ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(process_file, path): path for path in file_paths}
            for future in as_completed(future_to_file):
                try:
                    filename, tokenlist = future.result()
                    filelist.append([filename, tokenlist])
                except Exception as e:
                    print(f"An error occurred while processing a file: {e}")
        
        print("get filelist")
        print(filelist)
        
        # 結果をレンダリング
        return render_template('token.html', filelist=filelist, analysis_method="search frequency token", token_num=token_num)
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500
    

@app.route('/display/search', methods=['POST'])
def search_display():
    return render_template('display.html', type=request.form.get("type"))
    

@app.route('/token/search', methods=['POST'])
def token_search():
    try:
        keyword=request.form.get("keyword")
        print("success access /token/search")
        selected=request.form.getlist("option")
        filelist=[]
        for filename in selected:
            filepath=os.path.join('uploads', filename)
            sentence_list=analysis.token_search(keyword, filepath)

            if sentence_list is None:
                sentence_list=[]
                print("sentence is none")
            filename="".join(filename)
            filelist.append([filename, sentence_list])
            
        return render_template('token.html', filelist=filelist, analysis_method="token_search", keyword=keyword)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500


    


if __name__ == '__main__':
    app.run(debug=True)
