from flask import Flask, render_template, request, redirect, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)
mongo = MongoClient(‘localhost’,27017)
db = mongo.pratice

app.config["UPLOAD_FOLDER"]= ‘imgupl'

@app.route(‘/’)
def index():
    return render_template(‘index.html’,users=user)

@app.route(‘/signup’)
def signup():
    return render_template(‘signup.html’)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username', 0)
        password = request.form.get('password', 0)
        if not (username and password):
            return 'Error'

        data = list(db.users.find({'username' : username}, {'password' : password}))
        if len(data):
            data = data[0]['password']
            print(data)
            if password == data:
                return render_template('login.html')
        return 'Error'

    return render_template('login.html')

ALLOWED_EXTENSIONS = {‘png’, 'gif', ‘jpg’, ‘jpeg’}
@app.route(‘/upload’,methods=[‘GET’,’POST’])
def imgupl(): 
    if request.method == ‘POST’:
        this_file = request.files[‘file’]
        
        if this_file in ALLOWED_EXTENSIONS:
            this_file.save(os.path.join(app.config[‘UPLOAD_FOLDER’],filename))
            return ‘Successfully uploaded’
        else:
            return (‘Error’)
    return render_template(‘imgupl.html’)

@app.route(‘/upload/<filename>‘)
def imguplfile(filename):
    return send_from_directory(app.config[‘UPLOAD_FOLDER’],filename)


if __name__ == ‘__main__’:
    app.run(host=‘localhost’, port=5000, debug=True)
