# このアプリの起動方法
## 環境構築
### Flask インストール
pip install flask
### jinja2 インストール
pip install jinja2
## 起動手順

git cloneした直後はすべて"Authorship_analasys"というファイルに入っているが、名前を変更して"flaskr"とする

自分の環境に合わせたターミナルに以下のコマンドを打てばよい
### For mac(bash)
export FLASK_APP=flaskr
export FLASK_ENV=development

### For Windows(cmd)
set FLASK_APP=flaskr
set FLASK_ENV=development

### For Windows(power shell)
$env:FLASK_APP="flaskr"
$env:FLASK_APP="development"