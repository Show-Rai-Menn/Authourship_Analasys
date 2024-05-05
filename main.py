from flask import render_template
from flaskr import app

@app.route('/')
def index():
    print("OK")
    return render_template('index.html')
