from cars_app import app
from flask import render_template, redirect, request
from cars_app.models.car import Car

#to use later for login and registration
@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    cars = Car.get_all()
    return render_template('dashboard.html', cars = cars)

@app.route('/cars/new')
def new_car():
    return render_template('new_car.html') #show form

@app.route('/cars/create', methods = ['POST'])
def create_car():
    # expecting a request.form
    # create a dictionary.... to pass into Car.save()
    data = {
            'color' : request.form['color'],
            'year' : request.form['year'],
            'maker_id' : request.form['maker_id'],
            'user_id' : session['user_id'],
        }
    Car.save(data)
    return redirect('/dashboard')
