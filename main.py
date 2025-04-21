import wcocr
import os
import uuid
import base64
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
wcocr.init("/app/wx/opt/wechat/wxocr", "/app/wx/opt/wechat")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        # 从formdata获取图片文件
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        image_file = request.files['image']
        if not image_file or image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # 创建临时目录
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 生成唯一文件名并保存图片
        filename = os.path.join(temp_dir, f"{str(uuid.uuid4())}.png")
        try:
            image_file.save(filename)

            # 使用OCR处理图片
            result = wcocr.ocr(filename)
            return jsonify({result})

        finally:
            # 清理临时文件
            if os.path.exists(filename):
                os.remove(filename)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)