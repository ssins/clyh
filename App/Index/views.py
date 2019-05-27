from App.Index import index
from flask import Flask, request, redirect, url_for, send_file, abort
from werkzeug import SharedDataMiddleware
from App.Index.controllers import *
@index.route('/', methods=['GET', 'POST'])
def upload_pic():
    if request.method == 'POST':
        file = request.files['file']
        path = upload_files(file)
        if path:
            return redirect(url_for('index.cal', path=path))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>材料优化</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=优化>
    </form>
    '''


@index.route('/cal', methods=['GET'])
def cal():
    path = request.args.get('path', '')
    if path:
        return cal_file(path)
    return '文件读取失败'


@index.route('/download', methods=['GET'])
def download():
    path = request.args.get('path', '')
    if request.method == "GET":
        if os.path.isfile(path):
            return send_file(path,as_attachment=True)
        abort(404)
