from books_app import app
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from books_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods = ['POST'])
def register():
    if not User.valid_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    return redirect('/books')

# Login
@app.route('/login', methods = ['POST'])
def login():
    if not User.valid_login(request.form):
        return redirect('/')
    user = User.get_one_by_email(request.form)
    session['user_id'] = user.id
    return redirect('/books')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')    