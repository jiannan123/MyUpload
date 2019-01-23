import os
from flask import Flask, render_template, send_from_directory, request, jsonify,flash

app = Flask(__name__)

UPLOAD_FOLDER = 'G:\\111\\back\\store\\'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
app.secret_key = '123'
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'rar', 'JPG', 'PNG', 'zip', 'gif', 'GIF'])  # 允许上传的文件后缀

# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 具有上传功能的页面

@app.route('/')
def upload_test():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    f=request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname=f.filename
        f.save(os.path.join(file_dir, fname))  #保存文件到upload目录
        flash("文件 %s 上传成功" % f.filename, 'ok')
        return render_template('index.html')
    else:
        flash("文件上传失败，无效的格式 %s" % f.filename.rsplit('.', 1)[1], 'err')
        return render_template('index.html')
@app.route("/download/<path:filename>")
def downloader(filename):
    dirpath = os.path.join(app.root_path, 'store')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载

if __name__ == '__main__':
    app.run(debug=True)