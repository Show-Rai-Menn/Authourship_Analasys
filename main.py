from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import os
from werkzeug.utils import secure_filename
import db
import search_token
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/up')
def upload_index():
    return render_template('upload.html', method='Upload')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))

        db.upload(filename, app.root_path)
        return redirect(url_for('index'))
    


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
def token():
    try:
        print("success access /token")
        selected=request.form.getlist("option")
        counter=int(request.form.get('counter'))
        
        filelist=[]
        for filename in selected:
            filepath=os.path.join("uploads", filename)
            print(counter*20)
            tokenlist=search_token.search_token(filepath, counter*20)
            if tokenlist is None:
                tokenlist=[]
                print("tokenlist is none")
            filelist.append(filename)
            filelist.append(tokenlist)
            print("get filelist")
            print(filelist)
        return render_template('token.html', filelist=filelist, analysis_method="search frequency token", token_num=counter*20)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500


    

if not os.path.exists('uploads'):
    os.makedirs('uploads')
if __name__ == '__main__':
    app.run(debug=True)
