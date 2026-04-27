import base64
import importlib
import io
import json
import logging
import os
import shutil
import uuid
from datetime import datetime

import numpy as np
import pymysql
import requests
import visual
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image
from process_text import split_paragraphs
from werkzeug.utils import secure_filename

try:
    import erniebot as _erniebot_module
except ImportError:
    _erniebot_module = None

try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
except ImportError:
    VideoFileClip = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None


class ErnieBotProxy:
    def __getattr__(self, name):
        return getattr(get_erniebot(), name)


class LazyModuleProxy:
    def __init__(self, module_name):
        self.module_name = module_name
        self._module = None
        self._error = None

    def _load(self):
        if self._module is not None:
            return self._module
        if self._error is not None:
            raise RuntimeError(f"Module '{self.module_name}' is unavailable: {self._error}") from self._error
        try:
            self._module = importlib.import_module(self.module_name)
            return self._module
        except Exception as exc:
            self._error = exc
            raise RuntimeError(f"Module '{self.module_name}' is unavailable: {exc}") from exc

    def __getattr__(self, name):
        return getattr(self._load(), name)


class MySQL:
    def __init__(self, app=None):
        self.app = None
        self._connection = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def _connect(self):
        if self.app is None:
            raise RuntimeError("Flask app is not configured for MySQL access.")
        return pymysql.connect(
            host=self.app.config["MYSQL_HOST"],
            user=self.app.config["MYSQL_USER"],
            password=self.app.config["MYSQL_PASSWORD"],
            database=self.app.config["MYSQL_DB"],
            charset="utf8mb4",
            autocommit=False,
        )

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._connect()
        else:
            self._connection.ping(reconnect=True)
        return self._connection


def get_erniebot():
    if _erniebot_module is None:
        raise RuntimeError("The 'erniebot' package is not installed.")
    _erniebot_module.api_type = os.getenv("ERNIEBOT_API_TYPE", "aistudio")
    _erniebot_module.access_token = os.getenv(
        "ERNIEBOT_ACCESS_TOKEN",
        "476cff13430cb3ecdf0b5437d331ff6b49ba0b9d",
    )
    return _erniebot_module


def ensure_dependency(name, value):
    if value is None:
        raise RuntimeError(f"The '{name}' package is not installed.")
    return value


DEFAULT_IE_SCHEMA = ["时间", "出发地", "目的地", "费用"]
erniebot = ErnieBotProxy()
Knowledge = LazyModuleProxy("Knowledge")
_ocr_engine = None
_asr_executor = None
_ie_engine = None
_ie_schema = tuple(DEFAULT_IE_SCHEMA)
DEFAULT_IE_SCHEMA = ["时间", "出发地", "目的地", "费用"]
_ie_schema = tuple(DEFAULT_IE_SCHEMA)

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST", "127.0.0.1")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER", "root")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD", "123456")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB", "editer_database")
app.secret_key = '@wudao'

CORS(app)
mysql = MySQL(app)

UPLOAD_FOLDER = 'load_wendang'  # 替换为服务器上的实际文件上传路径
KNOWLEDGE = 'knowledge'
STENCIL_FOLDER = 'stencil'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['KNOWLEDGE'] = KNOWLEDGE
app.config['STENCIL_FOLDER'] = STENCIL_FOLDER

erniebot.api_type = 'aistudio'
erniebot.access_token = '476cff13430cb3ecdf0b5437d331ff6b49ba0b9d'

# 初始化 ASR 和信息抽取任务
asr = None
schema = ["时间", "出发地", "目的地", "费用"]
ie = None

# 设置文件保存路径
audio_save_path = "work\\audio"
current_dir = os.getcwd()


def ensure_runtime_dirs():
    for relative_path in (
        UPLOAD_FOLDER,
        KNOWLEDGE,
        os.path.join(KNOWLEDGE, "audio"),
        os.path.join(KNOWLEDGE, "pdf"),
        os.path.join(KNOWLEDGE, "picture"),
        os.path.join(KNOWLEDGE, "video"),
        STENCIL_FOLDER,
        os.path.join("work", "audio"),
    ):
        os.makedirs(relative_path, exist_ok=True)


def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        from paddleocr import PaddleOCR

        _ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch")
    return _ocr_engine


def get_asr_executor():
    global _asr_executor
    if _asr_executor is None:
        from paddlespeech.cli.asr.infer import ASRExecutor

        _asr_executor = ASRExecutor()
    return _asr_executor


def get_ie_engine(schema=None):
    global _ie_engine, _ie_schema
    schema = tuple(schema or DEFAULT_IE_SCHEMA)
    if _ie_engine is None or _ie_schema != schema:
        from paddlenlp import Taskflow

        _ie_engine = Taskflow("information_extraction", schema=list(schema), task_path="work")
        _ie_schema = schema
    return _ie_engine


audio_save_path = os.path.join("work", "audio")
ensure_runtime_dirs()


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/api/entportal/v1/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'hwmsg': 'Username and password are required', 'hwcode': 1}), 200

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        user = cursor.fetchone()
        cursor.close()
        if user is None:
            print("1")
            return jsonify({'hwmsg': 'Invalid username or password', 'hwcode': 1}), 200

        avatar = user[5].decode('utf-8') if isinstance(user[5], bytes) else user[5]

        return jsonify({
            'hwmsg': 'User logged in successfully',
            'hwcode': 0,
            'hwdata': {
                'token': 'dummy_token',
                'user': {'name': user[1], 'role': user[3], 'avatar': avatar}
            }
        }), 200
    return 'false'


@app.route('/api/entportal/v1/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        image = 'data:application/octet-stream;base64,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'

        if not username or not email or not password or not role:
            return jsonify({'hwmsg': 'Username, email, password, and role are required', 'hwcode': 1}), 200

        cursor = mysql.connection.cursor()

        # 检查用户名是否已经存在
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cursor.fetchone() is not None:
            return jsonify({'hwmsg': 'Username already exists', 'hwcode': 1}), 200

        # 检查邮箱是否已经存在
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone() is not None:
            return jsonify({'hwmsg': 'Email already exists', 'hwcode': 1}), 200

        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s)', (username, password, role, email, image))
        cursor.execute('INSERT INTO chat VALUES (NULL, %s, %s, %s)', (username, 0, ''))
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'hwmsg': 'User registered successfully',
            'hwcode': 0,
            'hwdata': {
                'token': 'dummy_token',
                'user': {'name': username, 'role': role}
            }
        }), 200
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/save', methods=['POST'])
def save():
    if request.method == 'POST':
        username = request.json.get('username')
        file_name = request.json.get('file_name')
        html_content = request.json.get('text')  # 获取前端传来的带HTML格式的文本内容
        content_size_bytes = len(html_content.encode('utf-8'))  # 获取html_content的大小（以字节为单位）
        # 将字节转换为KB
        content_size_kb = content_size_bytes / 1024  # 转换为KB

        # 如果大于1000KB，则显示为MB（保留一位小数），否则显示为KB
        if content_size_kb > 1000:
            content_size_mb = content_size_kb / 1000  # 转换为MB
            size = f"{round(content_size_mb, 1)}MB"
        else:
            size = f"{round(content_size_kb, 1)}KB"

        cursor = mysql.connection.cursor()

        cursor.execute('''
            SELECT file_path FROM Documents 
            WHERE name = %s AND user_id = (SELECT id FROM Users WHERE username = %s)
        ''', (file_name, username,))
        result = cursor.fetchone()
        if result:
            # 将HTML内容写入到相对应的文件地址中
            file_path = result[0]
            with open(file_path, 'w') as file:
                file.write(html_content)

            cursor.execute('''
                               UPDATE Documents 
                               SET name = %s, last_modified_time = %s, size = %s
                               WHERE file_path = %s 
                           ''', (file_name, datetime.now(), size, file_path,))
        else:
            unique_filename = str(uuid.uuid4()) + '.txt'  # 使用UUID生成唯一的文件名
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            star = 'false'
            with open(file_path, 'w') as file:
                file.write(html_content)
            cursor = mysql.connection.cursor()
            cursor.execute('''
                           INSERT INTO Documents (user_id, file_path, name, type, last_modified_time, size, star) 
                           SELECT id, %s, %s, %s, %s, %s, %s FROM Users WHERE username = %s
                       ''', (file_path, file_name, 'doc', datetime.now(), size, star, username,))
        mysql.connection.commit()
        cursor.close()
        print('Document successfully save')
        return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/open_document', methods=['GET'])
def open_document():
    if request.method == 'GET':
        username = request.args.get('username')
        file_name = request.args.get('file_name')
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT file_path FROM Documents JOIN Users ON Documents.user_id = Users.id 
            WHERE username = %s AND name = %s
        ''', (username, file_name,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            file_path = result[0]
            with open(file_path, 'r') as file:
                content = file.read()
            print('Document successfully fetched')
            return jsonify({'hwcode': 0, 'hwdata': content, 'hwmsg': 'Success'})
        else:
            return jsonify({'hwcode': 1, 'hwdata': None, 'hwmsg': 'Failed'})


@app.route('/api/check_documents', methods=['GET'])
def check_documents():
    if request.method == 'GET':
        username = request.args.get('username')
        file_name = request.args.get('file_name')
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM Documents JOIN Users ON Documents.user_id = Users.id WHERE username = %s AND name = %s',
            (username, file_name,))
        files = cursor.fetchall()
        cursor.close()
        if files:
            return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
        else:
            return jsonify({'hwcode': 0, 'hwdata': 'false', 'hwmsg': 'No documents found'})


@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.json.get('username')
            file_name = request.json.get('file_name')
            file_type = request.json.get('file_type')
            file_extension = 'txt'
            unique_filename = str(uuid.uuid4()) + '.' + file_extension  # 使用UUID生成唯一的文件名
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            star = 'false'
            size = '0MB'
            # last_modified = request.form.get('last_modified_time')
            with open(file_path, 'w') as file:
                file.write('')

            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO Documents (user_id, file_path, name, type, last_modified_time, size, star) 
                SELECT id, %s, %s, %s, %s, %s, %s FROM Users WHERE username = %s
            ''', (file_path, file_name, file_type, datetime.now(), size, star, username,))
            mysql.connection.commit()
            cursor.close()
            print('Document successfully uploaded')
        return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/update_star', methods=['POST'])
def update_star():
    if request.method == 'POST':
        doc_id = request.json.get('doc_id')
        new_star = request.json.get('new_star')
        if new_star == 1:
            new_star = 'true'
        else:
            new_star = 'false'
        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE Documents SET star = %s WHERE id = %s',
            (new_star, doc_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/download', methods=['GET'])  # 还有些问题
def download():
    if request.method == 'GET':
        username = request.args.get('username')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT file_path FROM Documents JOIN Users ON Documents.user_id = Users.id WHERE username = %s',
                       (username,))
        files = cursor.fetchall()
        cursor.close()
        if files:
            print('Documents successfully fetched')
            return str(files)
        else:
            return 'false'


@app.route('/api/update_avatar', methods=['POST'])
def update_avatar():
    if request.method == 'POST':
        username = request.form.get('username')
        avatar_base64 = request.form.get('avatar')  # 获取用户上传的base64编码的头像
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Users SET image = %s WHERE username = %s
        ''', (avatar_base64, username,))
        mysql.connection.commit()
        cursor.close()
        print('Avatar successfully updated')
        return jsonify({'hwcode': 0, 'hwdata': 0, 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 1, 'hwmsg': 'Failed'})


@app.route('/api/get_avatar', methods=['POST'])
def get_avatar():
    if request.method == 'POST':
        username = request.json.get('username')
        cursor = mysql.connection.cursor()
        cursor.execute('''
            select image from Users  WHERE username = %s
        ''', (username,))
        image = cursor.fetchone()[0]
        mysql.connection.commit()
        cursor.close()
        print('Avatar successfully updated')
        return jsonify({'hwcode': 0, 'hwdata': image, 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 1, 'hwmsg': 'Failed'})


@app.route('/api/get_documents', methods=['GET'])
def get_all_documents():
    if request.method == 'GET':
        username = request.args.get('username')
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT documents.id, name, file_path, last_modified_time, size, star FROM Documents JOIN Users ON '
            'Documents.user_id = Users.id WHERE username = %s ORDER BY last_modified_time DESC',
            (username,))
        files = cursor.fetchall()
        cursor.close()
        if files:
            print('Documents successfully fetched')
            files_dict = [
                {'id': file[0], 'name': file[1], 'file_path': file[2], 'last_modified_time': file[3], 'size': file[4],
                 'star': file[5]} for
                file in files]
            return jsonify({'hwcode': 0, 'hwdata': {'documents': files_dict}, 'hwmsg': 'Success'})
        else:
            return jsonify({'hwcode': 1, 'hwdata': None, 'hwmsg': 'No documents found'})


@app.route('/api/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        data = request.get_json()  # 获取请求体中的 JSON 数据
        username = data.get('username')
        file_name = data.get('file_name')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                    SELECT file_path FROM Documents 
                    WHERE user_id = (SELECT id FROM Users WHERE username = %s) AND name = %s
                ''', (username, file_name,))
        file_path = cursor.fetchone()[0]  # 获取查询结果
        os.remove(file_path)  # 从服务器删除文件
        cursor.execute('''
            DELETE FROM Documents 
            WHERE user_id = (SELECT id FROM Users WHERE username = %s) AND name = %s
        ''', (username, file_name,))
        mysql.connection.commit()
        cursor.close()
        print('Document successfully deleted')
        return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/query', methods=['GET'])
def query():
    if request.method == 'GET':
        username = request.args.get('username')
        file_name = request.args.get('file_name')
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT name, type, file_path, last_modified_time FROM Documents JOIN Users ON Documents.user_id = Users.id WHERE username = %s AND name = %s',
            (username, file_name,))
        files = cursor.fetchall()
        cursor.close()
        if files:
            print('Documents successfully searched')
            files_dict = [{'name': file[0], 'type': file[1], 'file_path': file[2], 'last_modified_time': file[3]} for
                          file in files]
            return jsonify({'hwcode': 0, 'hwdata': files_dict, 'hwmsg': 'Success'})
        else:
            return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/upload_stencil', methods=['POST'])
def upload_stencil():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        file_name = data.get('file_name')
        name = data.get('name')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                    SELECT * FROM stencil WHERE name = %s and username = %s
            ''', (file_name, username))
        query = cursor.fetchone()
        if query:
            return jsonify({'hwcode': 0, 'hwdata': 'false', 'hwmsg': 'Stencils have existed'})
        cursor.execute('''
                    SELECT file_path FROM Documents JOIN Users ON Documents.user_id = Users.id 
                    WHERE username = %s AND name = %s
                ''', (username, file_name,))
        file_path = cursor.fetchall()[0]
        print(file_path[0])
        # label = des_info.get('label')
        # description = des_info.get('description')
        if data.get('label'):
            label = data.get('label')
        else:
            label = '无'
        if data.get('description') and data.get('description') != '':
            description = data.get('description')
        else:
            description = '这里空空如也~'
        unique_filename = str(uuid.uuid4()) + '.' + 'txt'  # 使用UUID生成唯一的文件名
        path = os.path.join(app.config['STENCIL_FOLDER'], unique_filename)
        with open(file_path[0], 'r') as sf:
            content = sf.read()
        with open(path, 'w') as tf:
            tf.write(content)
        cursor.execute('''
            INSERT INTO stencil (username, name, path, description, label, create_time, update_time ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (username, name, path, description, label, datetime.now(), datetime.now()))
        mysql.connection.commit()
        cursor.close()
        print('Stencil successfully uploaded')
        return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Failed'})


@app.route('/api/open_stencil', methods=['GET'])
def open_stencil():
    if request.method == 'GET':
        username = request.args.get('username')
        name = request.args.get('name')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT path FROM stencil WHERE username = %s and name = %s', (username, name))
        file_path = cursor.fetchone()[0]
        cursor.close()
        if file_path:
            print('Stencil successfully fetched')
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            return jsonify({'hwcode': 0, 'hwdata': file_content, 'hwmsg': 'Success'})
        else:
            return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Failed'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Failed'})


@app.route('/api/get_all_stencil', methods=['GET'])
def get_all_stencil():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM stencil")
        stencils = cursor.fetchall()
        stencil_list = []
        for stencil in stencils:
            stencil_dict = {
                'id': stencil[0],
                'username': stencil[1],
                'title': stencil[2],
                'description': stencil[4],
                'label': stencil[5],
                'create_time': stencil[6].strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': stencil[7].strftime('%Y-%m-%d %H:%M:%S')
            }
            stencil_list.append(stencil_dict)

        cursor.execute("SELECT * FROM Videos")
        videos = cursor.fetchall()
        cursor.close()
        for video in videos:
            video_dict = {
                'id': video[0],
                'title': video[1],
                'description': video[2],
                'label': video[4],
                'username': video[5],
                'create_time': video[6].strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': video[7].strftime('%Y-%m-%d %H:%M:%S')
            }
            stencil_list.append(video_dict)

        return jsonify({'hwcode': 0, 'hwdata': stencil_list, 'hwmsg': 'Success'}), 200
    else:
        return jsonify({'hwcode': 1, 'hwdata': None, 'hwmsg': 'Failed'})


@app.route('/api/start-collaboration', methods=['POST'])
def start_collaboration():
    if request.method == 'POST':
        data = request.get_json()
        share_code = data.get('shareCode')
        username = data.get('username')
        color = data.get('color')
        user_info = json.dumps([{'username': username, 'color': color}])
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO collaborations (share_code, usernames) VALUES (%s, %s)',
                       (share_code, user_info,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({
            'hwmsg': 'User start collaboration successfully',
            'hwcode': 0,
        }), 200
    return jsonify({'hwmsg': 'error', 'hwcode': 1}), 200


@app.route('/api/close-collaboration', methods=['POST'])
def close_collaboration():
    if request.method == 'POST':
        data = request.get_json()
        share_code = data.get('shareCode')
        cursor = mysql.connection.cursor()
        cursor.execute('delete collaborations from collaborations where share_code=%s',
                       (share_code,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({
            'hwmsg': 'User close collaboration successfully',
            'hwcode': 0,
        }), 200
    return jsonify({'hwmsg': 'error', 'hwcode': 1}), 200


@app.route('/api/join-collaboration', methods=['POST'])
def join_collaboration():
    if request.method == 'POST':
        data = request.get_json()
        share_code = data.get('shareCode').strip()
        username = data.get('username')
        color = data.get('color')
        user_info = {'username': username, 'color': color}
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT usernames FROM collaborations WHERE share_code = %s', (share_code,))
        result = cursor.fetchone()

        if result:
            usernames = json.loads(result[0])
            usernames.append(user_info)
            cursor.execute('UPDATE collaborations SET usernames = %s WHERE share_code = %s',
                           (json.dumps(usernames), share_code,))
            mysql.connection.commit()
            cursor.close()
        else:
            mysql.connection.commit()
            cursor.close()
            return jsonify({'hwmsg': 'sharecode error', 'hwcode': 1}), 200

        return jsonify({
            'hwmsg': 'User joined collaboration successfully',
            'hwcode': 0,
            'hwdata': {
                'shareCode': share_code,
                'user': {'name': username}
            }
        }), 200
    return jsonify({'hwmsg': 'error', 'hwcode': 1}), 200


@app.route('/api/quit-collaboration', methods=['POST'])
def quit_collaboration():
    if request.method == 'POST':
        data = request.get_json()
        share_code = data.get('shareCode').strip()
        username = data.get('username')
        color = data.get('color')
        user_info = {'username': username, 'color': color}
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT usernames FROM collaborations WHERE share_code = %s', (share_code,))
        result = cursor.fetchone()

        if result:
            usernames = json.loads(result[0])
            if user_info in usernames:
                usernames.remove(user_info)
            cursor.execute('UPDATE collaborations SET usernames = %s WHERE share_code = %s',
                           (json.dumps(usernames), share_code,))
            mysql.connection.commit()
            cursor.close()
        else:
            mysql.connection.commit()
            cursor.close()
            return jsonify({'hwmsg': 'sharecode error', 'hwcode': 1}), 200

        return jsonify({
            'hwmsg': 'User quit collaboration successfully',
            'hwcode': 0,
            'hwdata': {
                'shareCode': share_code,
                'user': {'name': username}
            }
        }), 200
    return jsonify({'hwmsg': 'error', 'hwcode': 1}), 200


@app.route('/api/get-users', methods=['GET'])
def get_users():
    share_code = request.args.get('shareCode')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT usernames FROM collaborations where share_code =%s', (share_code,))
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    users = [json.loads(row[0]) for row in result]
    return jsonify({
        'hwmsg': 'success',
        'hwcode': 0,
        'hwdata': {
            'user': users,
        }
    }), 200


@app.route("/api/extend", methods=["POST"])
def extend_with_ernie():
    # 从前端获取用户输入的文本
    user_input = request.json["user_input"]
    message_extend = [{"role": "user", "content": user_input}]
    style = request.json["style"]
    length = request.json["length"]
    system = "你是一个文章、文本续写的专家，现在，我将给定你一段文字，你需要依据我所给的文字进行续写，要求总体与所给文字向贴切，语言风格为" + style + "限定" + length + "字以内，并且不需要额外回答，直接给出续写的内容即可。"
    # 调用百度API
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message_extend,
    )
    result = response.get_result()
    print(result)
    message_extend.clear()
    return jsonify({'hwcode': 0, 'hwdata': result, 'hwmsg': 'Success'})


@app.route("/api/polish", methods=["POST"])
def polish_with_ernie():
    # 从前端获取用户输入的文本
    user_input = request.json["user_input"]
    message_polish = [{"role": "user", "content": user_input}]
    style = request.json["style"]
    system = "你是一个文本润色的专家，现在，我将给定你一段文字，你需要将我所给的文字加以润色，要求语言风格为" + style + "并且重新进行排版。生成的内容用{}括起来。"
    # 调用百度API进行文本润色
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message_polish,
    )
    result = response.get_result()
    print(result)
    message_polish.clear()
    return jsonify({'hwcode': 0, 'hwdata': result, 'hwmsg': 'Success'})


@app.route("/api/transplate", methods=["POST"])
@app.route("/api/translate", methods=["POST"])
def transplate_with_ernie():
    # 从前端获取用户输入的文本
    user_input = request.json["text"]
    target_language = request.json["target_language"]
    message_transplate = [{"role": "user", "content": user_input}]
    system = "你是一个精通各国语言的翻译官，现在，我将给定你一段文字，你需要将我所给的语句翻译成" + target_language + "。注意，你只需要返回翻译结果，不需要回复额外字词。"
    # 调用百度API
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message_transplate,
    )
    result = response.get_result()
    print(result)
    message_transplate.clear()
    return jsonify({'hwcode': 0, 'hwdata': result, 'hwmsg': 'Success'})


@app.route("/api/abstracts", methods=["POST"])
def abstracts_with_ernie():
    # 从前端获取用户输入的文本
    user_input = request.json["text"]
    message_abstracts = [{"role": "user", "content": user_input}]
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system="你是一个提取文章、文本信息的专家，现在，我将给定你一段文字，你需要依据我所给的文字进行信息提取，并整合成摘要给我。注意，你只需要返回摘要，不需要回复额外字词。",
        messages=message_abstracts,
    )
    result = response.get_result()
    print(result)
    message_abstracts.clear()
    return jsonify({'hwcode': 0, 'hwdata': result, 'hwmsg': 'Success'})


@app.route("/api/modify", methods=["POST"])
def modify_with_ernie():
    # 从前端获取用户输入的文本
    user_input = request.json["text"]
    message_modify = [{"role": "user", "content": user_input}]
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=" 你是一个纠正病句错字的专家，现在，我将给定你一段文字，你需要对我所给的文字进行更正。",
        messages=message_modify,
    )
    result = response.get_result()
    message_modify.clear()
    return jsonify({'hwcode': 0, 'hwdata': result, 'hwmsg': 'Success'})


@app.route('/api/sort', methods=['POST'])
def process_text():
    data = request.get_json()  # 获取前端发送的JSON数据
    html_text = data['text']  # 从JSON数据中提取html_text
    processed_paragraphs = split_paragraphs(html_text)  # 分割段落
    if processed_paragraphs:
        return jsonify({
            'hwmsg': 'success',
            'hwcode': 0,
            'hwdata': processed_paragraphs,
        }), 200
    else:
        return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/ocr', methods=['POST'])
def ocr_api():
    # 检查是否有文件被提交
    username = request.form.get('username')
    file_name = request.form.get('file_name')
    cursor = mysql.connection.cursor()
    for key in request.files.keys():
        file = request.files[key]
        if file:
            filename = file.filename
            cursor.execute('select * from picture where username = %s and name = %s and file_name = %s',
                           (username, filename, file_name,))
            exist_flag = cursor.fetchone()
            if exist_flag:
                return jsonify({'hwcode': 0, 'hwdata': 'false', 'hwmsg': 'Success'})
            unique_filename = str(uuid.uuid4()) + '.' + 'txt'  # 使用UUID生成唯一的文件名
            file_path = os.path.join("knowledge/picture", unique_filename)
            file_path = file_path.replace('\\', '/')

            # 打开并读取图片z
            img = Image.open(file.stream)
            img = np.array(img)  # 将 PIL.Image 对象转换为 numpy.ndarray

            # 将numpy数组转换为字节流
            img_bytes = io.BytesIO()
            Image.fromarray(img).save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            # 将字节流转换为base64编码
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

            # 保存base64编码到文件
            with open(file_path, 'w') as f:
                f.write(img_base64)

            # 初始化OCR模型
            ocr = get_ocr_engine()

            # 进行OCR识别
            result = ocr.ocr(img, cls=True)
            text = ""
            for idx in range(len(result)):
                res = result[idx]
                for line in res:
                    # 只获取识别出来的文字，不包括确信度，并且只保留置信度大于或等于90的结果
                    if line[1][1] >= 0.9:
                        text += line[1][0] + '\n'
            cursor.execute('INSERT INTO picture VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)',
                           (username, filename, file_path, file_name, text, datetime.now(), 'false'))

            cursor.execute('select id from picture where path = %s', (file_path,))
            id = cursor.fetchone()
            mysql.connection.commit()

    cursor.close()
    return jsonify({
        'hwcode': 0,
        'hwdata': {
            'text': text,
            'Id': id,
        },
        'hwmsg': 'Success'})


@app.route('/api/ocr_delete', methods=['POST'])
def ocr_delete():
    file_name = request.form.get('file_name')
    username = request.form.get('username')
    name = request.form.get('name')
    cursor = mysql.connection.cursor()
    cursor.execute('''
                       SELECT path FROM picture
                       WHERE username = %s AND file_name = %s AND name = %s
                   ''', (username, file_name, name))
    file_path = cursor.fetchone()[0]  # 获取查询结果
    os.remove(file_path)  # 从服务器删除文件
    cursor.execute('''
                   DELETE FROM picture
                   WHERE username = %s AND file_name = %s AND name = %s
               ''', (username, file_name, name))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'hwcode': 0, 'hwdata': 'success', 'hwmsg': 'Picture successfully deleted'}), 200


# 处理上传的音频文件并进行信息抽取
def audio_ie(audio_path):
    asr_result = get_asr_executor()(audio_file=audio_path, force_yes=True)
    ie_result = get_ie_engine()(asr_result)
    return ie_result


def audio(audio_path):
    asr_result = get_asr_executor()(audio_file=audio_path, force_yes=True)
    message = [{"role": "user", "content": asr_result}]
    system = "你是一个语音识别、添加标点符号的专家。现在，我将给你一段没有标注标点符号的文本，你需要且只需要返回其标注了标点符号后的结果，不许额外回复。"
    # 调用百度API
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message,
    )
    asr_result = response.get_result()
    return asr_result


@app.route('/api/audioIE', methods=['POST'])
def audioIE():
    os.makedirs(audio_save_path, exist_ok=True)
    if request.files and 'file' in request.files:
        file = request.files['file']
    username = request.form.get('username')
    file_name = request.form.get('file_name')
    filename = request.form.get('filename')
    cursor = mysql.connection.cursor()
    cursor.execute('select * from audio where username = %s and name = %s and file_name = %s',
                   (username, filename, file_name,))
    exist_flag = cursor.fetchone()
    if exist_flag:
        return jsonify({'hwcode': 0, 'hwdata': 'false', 'hwmsg': 'Success'})
    file_extension = 'wave'
    unique_filename = str(uuid.uuid4()) + '.' + file_extension  # 使用UUID生成唯一的文件名
    path = os.path.join("knowledge/audio", unique_filename)
    path = path.replace('\\', '/')
    file.save(path)
    ie_result = audio(path)

    unique_filename1 = str(uuid.uuid4()) + '.' + 'txt'  # 使用UUID生成唯一的文件名
    file_path = os.path.join("knowledge/audio", unique_filename1)
    file_path = file_path.replace('\\', '/')
    # 打开并读取音频文件
    with open(path, 'rb') as f:
        audio_bytes = f.read()

    # 将字节流转换为base64编码
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    os.remove(path)

    with open(file_path, 'w') as f:
        f.write(audio_base64)

    cursor.execute('INSERT INTO audio VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)',
                   (username, file_name, filename, file_path, ie_result, datetime.now(), 'false'))

    cursor.execute('select id from audio where path = %s', (file_path,))
    id = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    print(ie_result)
    return jsonify({'hwcode': 0, 'hwdata': {'ie_result': ie_result, 'Id': id}, 'hwmsg': 'Success'})


@app.route('/api/audio_delete', methods=['POST'])
def audio_delete():
    file_name = request.form.get('file_name')
    username = request.form.get('username')
    name = request.form.get('name')
    print(file_name, username, name)
    cursor = mysql.connection.cursor()
    cursor.execute('''
                       SELECT path FROM audio
                       WHERE username = %s AND file_name = %s AND name = %s
                   ''', (username, file_name, name))
    file_path = cursor.fetchone()[0]  # 获取查询结果
    os.remove(file_path)  # 从服务器删除文件
    cursor.execute('''
                   DELETE FROM audio 
                   WHERE username = %s AND file_name = %s AND name = %s
               ''', (username, file_name, name))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'hwcode': 0, 'hwdata': 'success', 'hwmsg': 'Audio successfully deleted'}), 200


@app.route('/api/modifyIE', methods=['POST'])
def modifyIE():
    custom_schema = request.get_json()
    if custom_schema:
        # 第一个元素是信息内容
        content = custom_schema[0]
        # 后面的元素是关键词
        keywords = custom_schema[1:]
        print("Content:", content)
        print("Keywords:", keywords)

        # 更新信息抽取任务的 schema
        ie = get_ie_engine(keywords)

        # 对 content 进行信息抽取
        ie_result = ie(content)
        print("Information Extraction Result:", ie_result)
        return jsonify({'hwcode': 0, 'hwdata': ie_result, 'hwmsg': 'Schema updated successfully!'}), 200
    else:
        return jsonify({'hwcode': 1, 'hwdata': 'false', 'message': 'No schema provided.'}), 400


@app.route('/api/pdf_upload', methods=['POST'])
def pdf_upload():
    if request.files and 'file' in request.files:
        file = request.files['file']
    file_name = request.form.get('file_name')
    username = request.form.get('username')
    print(file_name, username)
    cursor = mysql.connection.cursor()

    cursor.execute('select * from audio where username = %s and name = %s',
                   (username, file_name,))
    exist_flag = cursor.fetchone()
    if exist_flag:
        return jsonify({'hwcode': 0, 'hwdata': 'false', 'hwmsg': 'Success'})

    file_path = Knowledge.pdfReader(file)

    cursor.execute('''
                   INSERT INTO knowledge (user_id, file_path, name, create_time, star) 
                   SELECT id, %s, %s, %s, %s FROM Users WHERE username = %s
               ''', (file_path, file_name, datetime.now(), 'false', username,))

    cursor.execute('select id from knowledge where file_path = %s', (file_path,))
    id = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    print('Document successfully uploaded')

    return jsonify({'hwcode': 0, 'hwdata': id, 'hwmsg': 'Success'})


@app.route('/api/pdf_delete', methods=['POST'])
def pdf_delete():
    file_name = request.form.get('file_name')
    username = request.form.get('username')
    cursor = mysql.connection.cursor()

    cursor.execute('''
                       SELECT file_path FROM knowledge 
                       WHERE user_id = (SELECT id FROM Users WHERE username = %s) AND name = %s
                   ''', (username, file_name,))
    file_path = cursor.fetchone()[0]  # 获取查询结果
    os.remove(file_path)  # 从服务器删除文件
    cursor.execute('''
                   DELETE FROM knowledge 
                   WHERE user_id = (SELECT id FROM Users WHERE username = %s) AND name = %s
               ''', (username, file_name,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'hwcode': 0, 'hwdata': 'success', 'hwmsg': 'Document successfully deleted'}), 200


@app.route('/api/get_datas', methods=['GET'])
def get_all_datas():
    if request.method == 'GET':
        username = request.args.get('username')
        file_name = request.args.get('file_name')
        cursor = mysql.connection.cursor()
        cursor.execute(
            'select * from audio where username = %s and file_name = %s',
            (username, file_name,))
        audio = cursor.fetchall()
        cursor.execute(
            'select * from picture where username = %s and file_name = %s',
            (username, file_name,))
        picture = cursor.fetchall()
        cursor.execute(
            'select * from knowledge JOIN Users ON knowledge.user_id = Users.id WHERE username = %s',
            (username,))
        pdf = cursor.fetchall()
        cursor.close()
        if audio or picture or pdf:
            print('Datas successfully fetched')
            audio_dict = [
                {'id': file[0], 'name': file[3], 'text': file[5], 'time': file[6], 'star': file[7],
                 'file': open(file[4], 'r').read()} for
                file in audio]
            picture_dict = [
                {'id': file[0], 'name': file[2], 'text': file[5], 'time': file[6], 'star': file[7],
                 'file': open(file[3], 'r').read()} for
                file in picture]
            pdf_dict = [
                {'id': file[0], 'name': file[3], 'time': file[4], 'star': file[5], } for
                file in pdf]
            return jsonify({'hwcode': 0, 'hwdata': {'audio': audio_dict, 'picture': picture_dict, 'pdf': pdf_dict},
                            'hwmsg': 'Success'})
        else:
            return jsonify({'hwcode': 1, 'hwdata': None, 'hwmsg': 'No documents found'})


@app.route('/api/update_kstar', methods=['POST'])
def update_kstar():
    if request.method == 'POST':
        file_id = request.form.get('id')
        file_type = request.form.get('type')
        print(file_id, file_type)
        cursor = mysql.connection.cursor()
        if file_type == 'image':
            cursor.execute(
                'select star from picture  WHERE id = %s',
                (file_id,))
            star = cursor.fetchone()[0]
            print(star)
            if star == 'false':
                star = 'true'
            else:
                star = 'false'
            cursor.execute('update picture set star = %s  where id = %s ', (star, file_id))
        elif file_type == 'audio':
            cursor.execute(
                'select star from audio  WHERE id = %s',
                (file_id,))
            star = cursor.fetchone()[0]
            print(star)
            if star == 'false':
                star = 'true'
            else:
                star = 'false'
            cursor.execute('update audio set star = %s  where id = %s ', (star, file_id))
        else:
            cursor.execute(
                'select star from knowledge  WHERE id = %s',
                (file_id,))
            star = cursor.fetchone()[0]
            print(star)
            if star == 'false':
                star = 'true'
            else:
                star = 'false'
            cursor.execute('update knowledge set star = %s  where id = %s ', (star, file_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'hwcode': 0, 'hwdata': 'true', 'hwmsg': 'Success'})
    return jsonify({'hwcode': 1, 'hwdata': 'false', 'hwmsg': 'Default'})


@app.route('/api/question', methods=['POST'])
def question():
    if request.method == 'POST':
        query = request.form.get('query')
        username = request.form.get('username')
        print(query, username)
        cursor = mysql.connection.cursor()
        cursor.execute('''
            select file_path from knowledge JOIN Users ON knowledge.user_id = Users.id WHERE username = %s and star = %s
        ''', (username, 'true'))
        files_path = cursor.fetchall()

        cursor.execute('''
                    select path from picture WHERE username = %s and star = %s
                ''', (username, 'true'))
        files_path += cursor.fetchall()

        cursor.execute('''
                            select path from picture WHERE username = %s and star = %s
                        ''', (username, 'true'))
        files_path += cursor.fetchall()
        print(files_path)
        if files_path:
            prompt = Knowledge.generate_prompt(query, files_path)
            print(prompt)
        else:
            prompt = "你是一个智能写作助手，你的名字叫文星星。"

        cursor.execute('''
                        select chat_number from chat where username = %s
                        ''', (username,))
        chat_num = cursor.fetchone()[0]
        print(chat_num)
        chat = []
        if chat_num <= 15 and chat_num >= 1:
            cursor.execute('''
                            select chat_memory from chat where username = %s
                            ''', (username,))
            chat_memory = json.loads(cursor.fetchone()[0])
            print(chat_memory)
            chat_num += 1
            chat.extend(chat_memory)
            chat.append({"role": "user", "content": query})
        else:
            chat = [{"role": "user", "content": query}]
            chat_num = 1

        response = erniebot.ChatCompletion.create(
            model='ernie-4.0',
            system=prompt,
            messages=chat,
        )
        result = response.get_result()
        chat.append({"role": "assistant", "content": result})
        chat_json = json.dumps(chat)
        cursor.execute('''
                          update chat set chat_number = %s, chat_memory = %s where username = %s
                       ''', (chat_num, chat_json, username,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'hwmsg': 'success',
            'hwcode': 0,
            'hwdata': result}), 200
    else:
        return jsonify({
            'hwmsg': 'failed',
            'hwcode': 1,
            'hwdata': 'false'}), 200


@app.route('/api/question_clear', methods=['GET'])
def question_clear():
    if request.method == 'GET':
        username = request.args.get('username')
        cursor = mysql.connection.cursor()
        cursor.execute('''
                        update chat set chat_number=0, chat_memory=''  where username = %s
                        ''', (username,))
        mysql.connection.commit()
        cursor.close()
    return jsonify({
        'hwmsg': 'success',
        'hwcode': 0,
        'hwdata': None}), 200


def audio_1(audio_path):
    asr_result = get_asr_executor()(audio_file=audio_path, force_yes=True)
    return asr_result


@app.route('/api/video_upload', methods=['POST'])
def video_upload():
    url = request.json.get('url')
    # 下载视频文件
    print(url)
    response = requests.get(url)
    unique = str(uuid.uuid4()) + '.'  # 使用UUID生成唯一的文件名
    video_file = unique + 'mp4'
    path = os.path.join("knowledge/video", video_file)
    path = path.replace('\\', '/')
    with open(path, 'wb') as f:
        f.write(response.content)

    # 使用 moviepy 提取音频
    video = ensure_dependency("moviepy", VideoFileClip)(path)
    audio_path = unique + 'wav'
    video.audio.write_audiofile(audio_path)

    # 使用 pydub 转换采样率
    audio1 = ensure_dependency("pydub", AudioSegment).from_wav(audio_path)
    audio1 = audio1.set_frame_rate(16000)
    audio_file = str(uuid.uuid4()) + '.wav'
    audio1_path = os.path.join("knowledge/video", audio_file)
    audio1.export(audio1_path, format='wav')

    audio2 = ensure_dependency("pydub", AudioSegment).from_wav(audio1_path)
    length = len(audio2)
    chunk_length = 50 * 1000  # 50秒
    chunks = [audio2[i:i + chunk_length] for i in range(0, length, chunk_length)]

    results = ""
    for i, chunk in enumerate(chunks):
        # 将音频段落保存为临时文件
        chunk_path = f"chunk_{i}.wav"
        chunk.export(chunk_path, format='wav')

        # 对音频段落进行语音识别
        result = audio_1(chunk_path)

        # 将结果添加到结果列表中
        results += result

        # 删除临时文件
        os.remove(chunk_path)
    print(results)
    message = [{"role": "user", "content": results}]
    system = "你是一个语音识别、添加标点符号并进行信息提炼的专家。现在，我将给你一段没有标注标点符号的文本，你需要添加标点符号并简练的概括这段文本。只返回概括后的结果，不许额外回复。"
    # 调用百度API
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message,
    )
    result = response.get_result()
    message.clear()
    print(result)

    return jsonify({'hwcode': 0, 'hwdata': result, 'hwmsg': 'Success'})


@app.route("/api/mindmap", methods=["POST"])
def mind_visual():
    # 从前端获取用户输入的文本
    user_input = request.json["user_input"]
    message_extend = [{"role": "user", "content": user_input}]
    system = '''
    你是一个专门生成思维导图的专家。对于我所给定你的每一段文本，你需要依据我所给的文本生成node_tree数据格式的思维导图，整个代码部分用{}括起来，在生成内容前加上：    
    "meta":{
        "name":"jsMind-demo-tree",
        "author":"hizzgdev@163.com",
        "version":"0.2"
    },

    /* 数据格式声明 */
    "format":"node_tree",
    。并只生成且只返回node_tree的代码。

    格式样例：
    {
    "meta": {
         "name": "英语学习路线",
         "author": "hizzgdev@163.com",
         "version": "0.2"
     },
     "format": "node_tree",
     "data": {
         "id": "英语学习路线",
         "topic": "英语学习路线",
         "children": [
             {
                 "id": "进阶阶段",
                 "topic": "进阶阶段",
                 "children": [
                 ...
                ]
            },
         ]
      }
}
切记，不需要返回额外内容。
    '''
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message_extend,
    )
    result = response.get_result()
    text = visual.mindmap(result)
    message_extend.clear()
    return jsonify({'hwcode': 0, 'hwdata': text, 'hwmsg': 'Success'})


@app.route("/api/visual_data", methods=["POST"])
def data_visual():
    # 从前端获取用户输入的文本
    user_input = request.form.get("user_input")
    type = request.form.get("type")
    message_extend = [{"role": "user", "content": user_input}]
    system = visual.v_style(type)
    # 调用百度API
    response = erniebot.ChatCompletion.create(
        model='ernie-4.0',
        system=system,
        messages=message_extend,
    )
    result = response.get_result()
    text = visual.mindmap(result)
    print(text)
    message_extend.clear()
    return jsonify({'hwcode': 0, 'hwdata': text, 'hwmsg': 'Success'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'doc', 'pdf', 'mp4', 'ogg', 'flv', 'avi', 'wmv',
                                                                      'rmvb'}


@app.route('/api/video/upload/chunk', methods=['POST'])
def upload_chunk():
    chunk_file = request.files['chunkFile']
    chunk_number = request.form.get('chunkNumber', 0, type=int)
    identifier = request.form.get('identifier')

    chunk_folder = os.path.join(app.config['STENCIL_FOLDER'], identifier)
    os.makedirs(chunk_folder, exist_ok=True)

    chunk_filename = f"{chunk_number}"
    chunk_save_path = os.path.join(chunk_folder, chunk_filename)

    chunk_file.save(chunk_save_path)
    return jsonify({'code': 200, 'msg': 'Chunk upload complete'})


@app.route('/api/video/checkName', methods=['POST'])
def check_video_name():
    data = request.get_json()
    title = data.get('title', '')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Videos WHERE title = %s LIMIT 1", [title])
    existing_video = cursor.fetchone()
    cursor.close()
    if existing_video:
        return jsonify({'code': 400, 'msg': 'File name already exists'})
    return jsonify({'code': 200, 'msg': 'File name available'})


@app.route('/api/video/merge', methods=['POST'])
def merge_video():
    try:
        data = request.get_json()
        file_info = data.get('fileInfo')
        video_info = data.get('videoInfo')

        # 打印 video_info 确认 username 是否在其中
        print(f"Received video info: {video_info}")

        identifier = file_info.get('uniqueIdentifier')
        filename = file_info.get('name')

        chunk_folder = os.path.join(app.config['STENCIL_FOLDER'], identifier)
        target_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(chunk_folder):
            return jsonify({'code': 400, 'msg': 'Chunk folder does not exist'})

        chunk_files = sorted(os.listdir(chunk_folder), key=lambda x: int(x))
        with open(target_file_path, 'wb') as target_file:
            for chunk_file in chunk_files:
                chunk_path = os.path.join(chunk_folder, chunk_file)
                if os.path.exists(chunk_path):
                    print(f"Merging chunk: {chunk_path}")  # 添加调试信息
                    with open(chunk_path, 'rb') as cf:
                        target_file.write(cf.read())
                        target_file.flush()  # 刷新输出缓冲区
                        os.fsync(target_file.fileno())  # 确保数据已经写入磁盘
                else:
                    print(f"Chunk file missing: {chunk_path}")
                    return jsonify({'code': 500, 'msg': f'Chunk file {chunk_file} is missing'})

        # Delete chunk folder after merge
        shutil.rmtree(chunk_folder)  # 使用 shutil.rmtree 删除目录

        # 创建新的视频记录
        title = video_info.get('title')
        description = video_info.get('description')
        video_addr = f"uploads/{filename}"
        label = video_info.get('label')
        username = video_info.get('userName')  # 确保此处正确存储了 username

        cursor = mysql.connection.cursor()
        insert_query = """
        INSERT INTO Videos (title, description, video_addr, label, username)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (title, description, video_addr, label, username))
        mysql.connection.commit()
        cursor.close()

        # 生成视频封面截图
        if allowed_file(filename) and filename.rsplit('.', 1)[1].lower() in {'mp4', 'ogg', 'flv', 'avi', 'wmv', 'rmvb'}:
            thumbnail_path = target_file_path.rsplit('.', 1)[0] + ".jpg"
            save_video_thumbnail(target_file_path, thumbnail_path)

        return jsonify({'code': 200, 'msg': 'File successfully merged'})
    except Exception as e:
        logging.error("Error during merging video", exc_info=True)
        return jsonify({'code': 500, 'msg': 'Internal Server Error', 'error': str(e)}), 500


@app.route('/api/uploads/<path:filename>')
def uploaded_file(filename):
    directory = app.config['UPLOAD_FOLDER']
    if os.path.exists(os.path.join(directory, filename)):
        return send_from_directory(directory, filename)
    else:
        return send_from_directory('static', '3.jpg')  # 提供默认图片路径


@app.route('/api/video/downloadVideo', methods=['GET'])
def download_video():
    video_url = request.args.get('videoUrl')
    directory, filename = os.path.split(video_url)
    return send_from_directory(directory, filename)


def save_video_thumbnail(video_path, thumbnail_path):
    clip = ensure_dependency("moviepy", VideoFileClip)(video_path)
    # 截取视频第2秒的帧作为封面
    clip.save_frame(thumbnail_path, t=2)
    clip.close()


@app.route('/get_all_stencil', methods=['GET'])
def get_all_stencil_alias():
    return get_all_stencil()


@app.route('/api/pdf_modifyIE', methods=['POST'])
def pdf_modify_ie():
    return modifyIE()


@app.route('/api/open_template', methods=['GET'])
def open_template():
    username = request.args.get('username')
    file_name = request.args.get('file_name')

    if not username or not file_name:
        return jsonify({'code': 400, 'msg': 'Missing username or file_name'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Videos WHERE username = %s AND title = %s LIMIT 1", (username, file_name))
    video = cursor.fetchone()
    cursor.close()

    if video:
        logging.info(f"Video found: {video}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video[3]))
        logging.info(f"Constructed file path: {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            return jsonify({'code': 200, 'file_path': content})
        else:
            logging.error(f'File not found at path: {file_path}')
            return jsonify({'code': 404, 'msg': 'File not found'}), 404
    else:
        logging.error(f'No matching template found for username: {username} and file_name: {file_name}')
        return jsonify({'code': 404, 'msg': 'Template not found'}), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
