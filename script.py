import base64
import json
import os

from flask import Flask, request, send_from_directory
import magic  # 需要安装python-magic库以检查文件MIME类型
import word2pdf
from gevent import pywsgi

# 安装 python-magic 库: pip install python-magic-bin (Windows) 或 pip install python3-magic (Linux/macOS)
magic = magic.Magic(mime=True)

with open('settings.json', 'r') as f:
    config = json.load(f)

# 获取当前工作目录（程序启动时的工作目录）
current_working_directory = os.getcwd()

UPLOAD_FOLDER = f"{current_working_directory}/resource/pdf"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

port = int(os.environ.get('PORT', config['server']['port']))

# 文件类型限定变量数组
file_type_array = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.ms-word.document.macroEnabled.12',
    'application/vnd.ms-word.template.macroEnabled.12',
    'application/vnd.ms-word',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'application/zip',
    'application/octet-stream'
]


# 处理上传的文件
@app.route('/api/word2pdf', methods=['POST'])
def handle_decoded_file():

    # 权限验证
    if request.headers.get('Authorization') != config['key']:
        return {"code": 401, "msg": "Invalid key"}

    encoded_data = request.form.get('doc_file')

    if not isinstance(encoded_data, str):
        return {"code": 400, "msg": "Invalid base64 encoded data"}

    decoded_data = base64.b64decode(encoded_data)

    # 检查解码后的数据是否为doc或docx文件
    file_type = magic.from_buffer(decoded_data)

    if file_type in file_type_array:
        # 提取或指定文件名后缀
        extension = '.docx'

        # 将文件内容写入磁盘
        docxName = word2pdf.generate_random_strings(12) + extension

        docxFilename = f"{current_working_directory}/resource/docx/{docxName}"

        with open(docxFilename, "wb") as f:
            f.write(decoded_data)

        pdfFilename = docxName.replace(extension, '.pdf')

        try:
            doc = word2pdf.convert_word_to_pdf(docxFilename, pdfFilename,
                                               output_path=f"{current_working_directory}/resource/pdf")
        except Exception as e:
            return {"code": 500, "msg": f"pdf文件转换失败，失败原因：{e}"}
        return {"code": 1, "file_url": request.host_url + f"resource/pdf/{pdfFilename}"}

    else:
        return {"code": 200, "msg": f"文件类型错误，文件类型为： {file_type}"}


# 用于下载pdf文件
@app.route('/resource/pdf/<path:filename>')
def download_file(filename):
    # 检查文件是否存在并且是安全的（这只是一个基本的安全检查）
    if filename and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                                   filename=filename,
                                   as_attachment=True, path='')  # 将其作为附件发送，以便浏览器显示为下载
    else:
        return f"The requested file does not exist.：{filename}", 404


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
