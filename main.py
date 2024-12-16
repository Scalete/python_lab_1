from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

trips = [
    {"country": "Turkey", "operator": "Operator1", "price": 1000, "days": 7},
    {"country": "Egypt", "operator": "Operator2", "price": 800, "days": 5},
    {"country": "Italy", "operator": "Operator3", "price": 1200, "days": 10},
    {"country": "Spain", "operator": "Operator4", "price": 900, "days": 6},
    {"country": "Greece", "operator": "Operator5", "price": 1100, "days": 8},
    {"country": "France", "operator": "Operator1", "price": 1300, "days": 9},
    {"country": "Japan", "operator": "Operator2", "price": 1500, "days": 12},
    {"country": "Australia", "operator": "Operator3", "price": 1700, "days": 14},
    {"country": "Thailand", "operator": "Operator4", "price": 950, "days": 7},
    {"country": "Brazil", "operator": "Operator5", "price": 1250, "days": 10}
]

@app.route('/')
def index():
    return render_template('index.html', trips=trips)

@app.route('/operator/<name>')
def by_operator(name):
    operator_trips = [trip for trip in trips if trip["operator"].lower() == name.lower()]
    if not operator_trips:
        return render_template('no_data.html')
    return render_template('operator.html', trips=operator_trips)

@app.route('/days/<int:n>')
def by_days(n):
    days_trips = [trip for trip in trips if trip["days"] >= n]
    if not days_trips:
        return render_template('no_data.html')
    return render_template('days.html', trips=days_trips)

@app.route('/expensive-turkey')
def expensive_turkey():
    turkey_trips = [trip for trip in trips if trip["country"].lower() == "turkey"]
    if not turkey_trips:
        return render_template('no_data.html')
    most_expensive = max(turkey_trips, key=lambda x: x['price'])
    return render_template('turkey.html', trip=most_expensive)


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    operator = request.form.get('operator')
    duration = request.form.get('duration')

    if not operator or not duration:
        flash('Please fill out all fields.', 'danger')
        return redirect(url_for('form'))

    # Фільтруємо поїздки за вибраними критеріями
    filtered_trips = [trip for trip in trips if trip["operator"] == operator]

    if duration == 'short':
        filtered_trips = [trip for trip in filtered_trips if trip["days"] <= 7]
    elif duration == 'long':
        filtered_trips = [trip for trip in filtered_trips if trip["days"] > 7]

    if not filtered_trips:
        flash('No trips found with the selected criteria.', 'warning')
        return redirect(url_for('form'))

    return render_template('results.html', trips=filtered_trips)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404