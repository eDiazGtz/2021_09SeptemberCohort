from cars_app.config.mysqlconnection import connectToMySQL

class Car:
    # Attributes
    def __init__(self, data): #constructor
        self.id = data['id']
        self.color = data['color']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        # results are the results from the DB
        results = connectToMySQL('cars_db').query_db(query)
        cars = []
        for car in results:
            cars.append(cls(car))
        return cars

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (color, year, created_at, updated_at, maker_id, user_id) VALUES (%(color)s, %(year)s, NOW(), NOW(), %(maker_id)s, %(user_id)s);"
        # results are the results from the DB
        return connectToMySQL('cars_db').query_db(query, data) # return the ID of the object inserted (created)
