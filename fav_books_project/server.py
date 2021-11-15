from books_app import app
# routes
from books_app.controllers import books_controller, users_controller

if __name__=="__main__":
    app.run(debug=True)