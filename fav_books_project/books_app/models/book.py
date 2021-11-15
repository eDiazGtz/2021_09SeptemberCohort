from books_app.config.mysqlconnection import connectToMySQL
from books_app.models import user
from flask import flash

class Book:
    db = "fav_books"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None #I expect a User object here
        self.likers = [] #users who like me

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.db).query_db(query)
        new_books = []
        if len(results) == 0:
            return new_books
        else:
            for book in results:
                new_books.append(cls(book))
            return new_books

    @classmethod
    def get_all_complete(cls):
        query = "SELECT * FROM books JOIN users ON books.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_books = []

        #getting each book dict
        for row in results:
            # goal one make book dict into book obj
            new_book = cls(row)
            # get user dictionary

            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            # goal two create user obj
            creator = user.User(user_data)
            # goal three add user obj into book obj
            new_book.creator = creator
            all_books.append(new_book)
        return all_books




    @classmethod
    def get_one_final_form(cls, data):
        # need book -- need creator -- need all likers
        query = "SELECT * FROM books JOIN users AS creator ON creator.id = books.user_id LEFT JOIN likes ON likes.book_id = books.id JOIN users AS likers ON likes.user_id = likers.id WHERE books.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query)
        # I NEED A BOOK OBJ
        book = cls(results[0])

        # I need creator data dictionary
        creator_data = {
                'id' : results[0]['creator.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'created_at' : results[0]['creator.created_at'],
                'updated_at' : results[0]['creator.updated_at'],
        }
        # I need creator obj
        creator_obj = user.User(creator_data)
        # I need to put creator user obj into book obj
        book.creator = creator_obj

        for liker in results:
            #need liker_data
            liker_data = {
                'id' : liker['liker.id'],
                'first_name' : liker['liker.first_name'],
                'last_name' : liker['liker.last_name'],
                'email' : liker['liker.email'],
                'password' : liker['liker.password'],
                'created_at' : liker['liker.created_at'],
                'updated_at' : liker['liker.updated_at'],
            }
            #need liker_obj
            liker_obj = user.User(liker_data)
            #need to add liker_obj to book.likers list
            book_likers_list = book.likers
            book_likers_list.append(liker_obj)

        return book







    @classmethod
    def save(cls, data):
        query = 'INSERT INTO books (title, description, created_at, updated_at, user_id) VALUES (%(title)s, %(description)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET title = %(title)s, description = %(description)s, updated_at = NOW() WHERE books.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    

    # @classmethod
    # def get_one(cls, data):
    #     query = 'SELECT * FROM books WHERE books.id = %(id)s'
    #     results = connectToMySQL(cls.db).query_db(query, data)
    #     book = cls(results[0])
    #     return book

    # we want to have our BOOK class handy
    @classmethod
    # we have class in cls  and we have data --- where we expect id
    def get_one(cls, data):
        query = 'SELECT * FROM books JOIN users ON books.user_id = users.id WHERE books.id = %(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results[0])
        # we need out book --- 
        book = cls(results[0])

        user_data = {
            'id' :          results[0]['users.id'],
            'first_name' :  results[0]['first_name'],
            'last_name' :   results[0]['last_name'],
            'email' :       results[0]['email'],
            'password' :    results[0]['password'],
            'created_at' :  results[0]['users.created_at'],
            'updated_at' :  results[0]['users.updated_at'],
        }
        # user object
        creator = user.User(user_data)
        # setting user object to book.creator
        book.creator = creator
        #return the filled out book. 
        return book

    
    @staticmethod
    def is_valid(data):
        #true or false
        is_valid = True
        if len(data['title']) < 1:
            flash('Title is required')
            is_valid = False
        if len(data['description']) < 5:
            flash('Description must be at least 5 characters')
            is_valid = False
        return is_valid