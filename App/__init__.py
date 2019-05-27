from flask import Flask
from config import MAX_CONTENT_LENGTH
from .Index import index
# >>import<< 代码自动生成标签，请勿删除或编辑本行


def create_app():
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(index, url_prefix='/index')
    # >>register<< 代码自动生成标签，请勿删除或编辑本行
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    return app
