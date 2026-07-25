from flask import *
from flask import render_template
from flask import request
from datetime import datetime
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
userBase = [
    {"name": "Kostia", "pas": "111", "email": "kost@gmail.com", "fname": "Kostua", "lname": "Sokirka", "age": "15"},
    {"name": "sfsf", "pas": "222",  "email": "sfsf@gmail.com", "fname": "FName2", "lname": "LName2", "age": "15"}
    ]

blog_posts = []

@socketio.on('my event')
def handle_my_custom_event(json):
    print('recived json: ' + str(json))

import time

def global_clock():
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        socketio.emit('clock_update', now) 
        socketio.sleep(1)

threading.Thread(target=global_clock).start()

@socketio.on('start_stopwatch')
def start_stopwatch():
    seconds = 0
    while True:
        time.sleep(1)
        seconds += 1
        emit('stopwatch_update', seconds)  

@app.route('/')
def index(): 
    return redirect(url_for('login'))
def cookies():
    UserName = request.form.get('username')
    resp = make_response('Ok')
    resp.set_cookie('UserName', UserName)
    
    

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if (request.form['username'] and
            request.form['password'] and
            request.form['firstname'] and
            request.form['lastname'] and
            request.form['email'] and
            request.form['age']):
            
            UserName = request.form['username']
            FirstName = request.form['firstname']
            LastName = request.form['lastname']
            Age = request.form['age']
            UserPas = request.form['password']
            Email = request.form['email']
            
            # Перевірка чи користувач вже є в базі
            for i in range(len(userBase)):
                if userBase[i]["name"] == UserName:
                    return render_template('unauthorized2.html')  # Якщо користувач вже є, виводимо помилку
            
            # Додаємо нового користувача
            newUser = {"name": UserName, "pas": UserPas, "email": Email, "fname": FirstName, "lname": LastName, "age": Age}
            userBase.append(newUser)
            return redirect(url_for("user", UserName=UserName))  # Перенаправляємо на профіль нового користувача
        
            resp = make_response('Ok')
            resp.set_cookie('UserName', UserName)
            
        else:
            return render_template('unauthorized2.html')  # Якщо не всі поля заповнені
    else:
        username = request.cookies.get('UserName', "")
        return render_template('registration.html', Username = username)

        
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        if (request.form['username'] and
            request.form['password'] and
            request.form['email']):
            UserName = request.form['username']
            UserPas = request.form['password']
            Email = request.form['email']
            for i in range(len(userBase)):
                if userBase[i]["name"] == UserName and userBase[i]['pas'] == UserPas and userBase[i]['email'] == Email:
                    return redirect(url_for("user", UserName = UserName, UserPas = UserPas, Email = Email))
                
            newUser = {"name": UserName, "pas": UserPas, "email": Email}
            
            UserName = request.form.get('username')
            resp = make_response('Ok')
            resp.set_cookie('UserName', UserName)
            username = request.cookies.get('UserName', "")
            
            print(userBase)
            abort(401)
    else:
        username = request.cookies.get('UserName', "")
        return render_template('login.html', username = username)

@app.route('/user/')
@app.route('/user/<UserName>', methods = ['POST', 'GET'])
def user(UserName = None, FirstName = None, LastName = None, Age = None):
    if UserName:
        for user in userBase:
            if user["name"] == UserName:
                FirstName = user["fname"]
                LastName = user["lname"]
                Age = user["age"]
                return render_template('profile.html', 
                                       UserName=UserName, 
                                       FirstName=FirstName, 
                                       LastName=LastName, 
                                       Age=Age)
    else:
        # Вивести всіх користувачів
        users_list = [{"UserName": user["name"], "FirstName": user["fname"], "LastName": user["lname"], "Age": user["age"]} for user in userBase]
        return render_template('all_users.html', users=users_list)
        
@app.route('/about_us')
def index2():
    return render_template('about_us.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        post = {
            "name": request.form.get("article_name"),
            "date": request.form.get("writing_date"),
            "author": request.form.get("article_author"),
            "topic": request.form.get("aritcle_topic"),
            "text": request.form.get("article_text")
        }

        blog_posts.append(post)
        print(blog_posts)

        socketio.emit('new_post', post)

        return redirect(url_for('blog'))

    return render_template('blog.html', posts=blog_posts)

@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized2.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found2.html'), 404

if __name__ == '__main__':
    socketio.run(app, debug = True, allow_unsafe_werkzeug = True)