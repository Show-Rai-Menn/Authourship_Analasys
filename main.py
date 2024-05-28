from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import os
from werkzeug.utils import secure_filename
import db
import analysis
app = Flask(__name__)

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/up')
def upload_index():
    return render_template('upload.html', method='Upload')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return render_template('upload.html', message='No file part', method='Upload')
    
    files = request.files.getlist('files')
    if not files:
        return render_template('upload.html', message='No selected file', method='Upload')
    
    
    
    for file in files:
        if file.filename == '':
            return render_template('upload.html', message='No selected file', method='Upload')#ファイル選択画面を開いたが何も選択していない場合
        
        
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            db.upload(filename, app.config['UPLOAD_FOLDER'])

        else:
            return render_template('upload.html', message='file extension is wrong', method='Upload')

    return render_template('upload.html', message='file upload successfully', method='Upload')
    


@app.route('/search/file')
def search():
    search_query = request.args.get('query', '')
    file_name=db.search(search_query)
    return jsonify([name[0] for name in file_name])

@app.route('/search')
def search_file():
    return render_template('search.html')

@app.route('/file')
def file_manage():
    filename=request.args.get('filename')
    return render_template('file_manage.html', filename=filename)

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
    return render_template('upload.html', method='Update')

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
        
        filelist=[]
        for filename in selected:
            filepath=os.path.join("uploads", filename)
            print(counter*20)
            tokenlist=analysis.token_frequency(filepath, counter*20)
            if tokenlist is None:
                tokenlist=[]#listの初期化
                print("tokenlist is none")
            filename="".join(filename)
            filelist.append([filename, tokenlist])#listの中に[filename, tokenlist]で値を格納
            
            print("get filelist")
            print(filelist)
        return render_template('token.html', filelist=filelist, analysis_method="search frequency token", token_num=counter*20)
    #ここではtoken.htmlはselect.htmlのid=resultに埋め込んでいる
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


    

if not os.path.exists('uploads'):
    os.makedirs('uploads')
if __name__ == '__main__':
    app.run(debug=True)
