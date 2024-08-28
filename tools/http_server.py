# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# requirement: pip install flask
# run this script, then open a browser and visit http://x.x.x.x:5000/form or http://x.x.x.x:5000/file

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # 获取表单数据
        data = request.form
        # 打印接收到的数据
        for key, value in data.items():
            print(f"{key}: {value}")
        # 返回响应
        return 'Data received!'
    else:
        # 如果是GET请求，显示一个简单的表单
        return '''
            <form method="post">
                <input type="text" name="username" placeholder="Username" />
                <input type="password" name="password" placeholder="Password" />
                <input type="submit" value="Submit" />
            </form>
        '''

@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/octet-stream':
            binary_data = request.data
            print("data:", len(binary_data))
            return jsonify({'message': 'Data received successfully'}), 200
    else:
        # 如果是GET请求，显示一个简单的表单
        return '''
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" value="Submit" />
            </form>
        ''' 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
