# このアプリの起動方法
## 環境構築
### Flask インストール
pip install flask
### jinja2 インストール
pip install jinja2
## 起動手順

git cloneした直後はすべて"Authorship_analasys"というファイルに入っているが、名前を変更して"flaskr"とする

flaskrファイルの1つ前のディレクトリに移動する

### 環境変数の保存
自分の環境に合わせたターミナルに以下のコマンドを打てばよい
下のコマンドは自分のPCに1時的に環境変数の保存をしている
#### For mac(bash)
export FLASK_APP=flaskr  
export FLASK_ENV=development

#### For Windows(cmd)
set FLASK_APP=flaskr  
set FLASK_ENV=development

#### For Windows(power shell)
$env:FLASK_APP="flaskr"  
$env:FLASK_APP="development"

### flask起動
flask run
