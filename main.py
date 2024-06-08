from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
import db
import analysis
from multiprocessing import Process
from collections import Counter
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


@app.route('/exploratory')
def exploratoryf():
    Q_file=db.search_allQ()
    K_files=db.search_allK()
    return render_template('exploratory.html', Q_file=Q_file, K_files=K_files)

@app.route('/exploratory/search', methods=['POST'])
def explonatory_search():
    data = request.get_json()
    search_type = data['searchType']
    search_term = data['searchTerm']
    Qfilenames = data.get('Q', [])
    Kfilenames = data.get('K', [])
    print(Qfilenames)
    context_size = 10
    Qcontents, Kcontents=db.get_content(Qfilenames, Kfilenames)

    if search_type == 'wordToken':
        Qresults, Kresults = exploratory.search_word_token(Qfilenames, Qcontents, Kfilenames, Kcontents, search_term, context_size)
    elif search_type == 'lemma':
        Qresults, Kresults = exploratory.search_lemma(Qfilenames, Qcontents, Kfilenames, Kcontents, search_term, context_size)
    elif search_type == 'pos':
        Qresults, Kresults = exploratory.search_pos(Qfilenames, Qcontents, Kfilenames, Kcontents, search_term, context_size)
    elif search_type == 'ngram':
        n = 3  # Default value for n-gram, can be adjusted as needed
        results = search_ngram(texts, search_term, n, context_size)
    elif search_type == 'regex':
        results = search_regex(texts, search_term, context_size)
    else:
        results = []
    
    rendered_html = render_template(
        'exploratory_result.html',
        Qresults=Qresults, Kresults=Kresults
    )
    return jsonify(html=rendered_html)

@app.route('/K_and_K')
def K_and_K():
    K_files=db.search_allK()
    
    return render_template('K_and_K.html',  K_files=K_files)
    
@app.route('/K_and_K/result', methods=['POST'])
def Kresult():
    Kfilename=request.form.getlist('K')
    null, Kfiles=db.get_content(None, Kfilename)
    
    result=analysis.K_and_K(Kfilename, Kfiles)
    print(type(result))
    return render_template('K_and_K_result.html', result=result, filenames=Kfilename)

@app.route('/comparison')
def comparison():
    Q_file=db.search_allQ()
    K_files=db.search_allK()
    return render_template('comparison.html', Q_file=Q_file, K_files=K_files)

@app.route('/comparison/result', methods=['POST'])
def comparison_Result():
    data = request.get_json()
    Qfilenames = data.get('Q', [])
    Kfilenames = data.get('K', [])
    count = data.get('count')
    print(Qfilenames)
    print(Kfilenames)
    
    Qcontents, Kcontents = db.get_content(Qfilenames, Kfilenames)
    token_num = count * 20
    Qresults = {}  # ファイルごとのトークントップリストを格納する辞書
    Kresults = {}

    if Qcontents:
        for content, filename in zip(Qcontents, Qfilenames):
            Qresults[filename] = analysis.token_frequency(content, token_num)
            
    if Kcontents:
        for content, filename in zip(Kcontents, Kfilenames):
            Kresults[filename] = analysis.token_frequency(content, token_num)
            print(type(Kresults[filename]))
            print(type(Kresults))
    
    # HTMLのレンダリング
    rendered_html = render_template(
        'comparison_result.html',
        Qresults=Qresults, Kresults=Kresults, token_num=token_num
    )
    return jsonify(html=rendered_html)
            
    


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
