import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

# 数据库连接
db = pymysql.connect('localhost', 'root', '123', 'test')
cursor = db.cursor()

# 后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')

#查
@app.route('/auth_user/all', methods=['POST'])
def all():
    if request.method == 'POST':
        cursor.execute('SELECT user_id,user_name,phone_number FROM auth_user;')
        data = cursor.fetchall()
        temp = {}
        result = []
        if (data != None):
            for i in data:

                temp['user_id'] = i[0]
                temp['user_name'] = i[1]
                temp['phone_number'] = i[2]
                result.append(temp.copy())
            print('result: ', len(data))
            return jsonify(result)
        else:
            print('result: NULL')
            return jsonify(result)

#增
@app.route('/auth_user/add', methods=['POST'])
def add():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
    try:
        cursor.execute('INSERT INTO auth_user(user_name,password,phone_number) VALUES(\'' + str(user_name) + '\',\''
                       + str(password) + '\',\'' + str(phone_number) + '\')')
        db.commit()
        print('add a new user succeed')
        return '1'
    except Exception as e:
        print('add a new user failed: ', e)
        db.rollback()
        return '-1'

#删
@app.route('/auth_user/del', methods=['POST'])
def dele():
    if request.method == 'POST':
        id = request.form.get('user_id')
    try:
        cursor.execute('DELETE FROM auth_user WHERE user_id =' + str(id))
        db.commit()
        print('delete  user succeed')
        return '1'
    except Exception as e:
        print('delete  user failed: ', e)
        db.rollback()
        return '-1'

#改
@app.route('/auth_user/update', methods=['POST'])
def update():
    if request.method == 'POST':
        name = request.form.get('user_name')
        password = request.form.get('password')
    try:
        cursor.execute(
            'UPDATE auth_user SET password =\'' + str(password) + '\' WHERE user_name = \'' + str(name) + '\'')
        db.commit()
        print('update successed')
        return '1'
    except Exception as e:
        print('update failed: ', e)
        db.rollback()
        return '-1'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8877)
    db.close()
    print('Goodbye!')
