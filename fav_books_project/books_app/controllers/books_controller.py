from flask import render_template, redirect, session, request, flash
from books_app import app
from books_app.models.book import Book
from books_app.models.user import User

################## NEED TO BE LOGGED IN ##########################

@app.route('/books')
def book_dash():
    if not 'user_id' in session:
        flash('You must be logged in to visit this page. Please Login or Register')
        redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_one(data)
    books = Book.get_all_complete()
    return render_template('books_dash.html', books=books, user=user)
    
@app.route('/books/create', methods=['POST', 'GET'])
def book_create():
    if not 'user_id' in session:
        flash('You must be logged in to visit this page. Please Login or Register')
        redirect('/')
    if request.method == 'GET':
        return redirect('/books')
    if not Book.is_valid(request.form):
        return redirect('/books')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'user_id' : session['user_id'],
    }
    Book.save(data)
    return redirect('/books')

@app.route('/books/<int:book_id>')
def book_one(book_id):
    if not 'user_id' in session:
        flash('You must be logged in to visit this page. Please Login or Register')
        redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_one(data)
    data = {
        'id' : book_id
    }
    book = Book.get_one(data)

    return render_template('books_one.html', user=user, book=book)

@app.route('/books/<int:book_id>/update', methods = ['POST'])
def book_update(book_id):
    if not 'user_id' in session:
        return redirect ('/')

    if not Book.is_valid(request.form):
        return redirect(f'/books/{book_id}')
    data = {
        'id' : book_id,
        'title' : request.form['title'],
        'description' : request.form['description'],
    }
    # update the book
    Book.update(data)
    return redirect(f'/books/{book_id}')