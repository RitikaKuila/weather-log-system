# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db=SQLAlchemy(app)

# class Weather(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.String(20), nullable=False)
#     temperature = db.Column(db.Float, nullable=False)
#     humidity = db.Column(db.Float, nullable=False)
# with app.app_context():
#     db.create_all()

# @app.route('/', methods=['GET', 'POST'])

# def index():
#     if request.method=='POST':
#         date=request.form['date']
#         temperature=request.form['temperature']
#         humidity=request.form['humidity']
#         new_log=Weather(date=date,temperature=temperature,humidity=humidity)
#         db.session.add(new_log)
#         db.session.commit()
#         return redirect('/')
#     logs= Weather.query.all()
#     return render_template('index.html', logs=logs)
# @app.route('/delete/<int:id>')
# def delete(id):
#     log= Weather.query.get(id)
#     db.session.delete(log)
#     db.session.commit()
#     return redirect('/')


# @app.route('/check-db')
# def check_db():
#     logs= Weather.query.all()
#     result= []
#     for log in logs:
#         result.append((log.id, log.date, log.temperature, log.humidity))
#     return str(result)


# if __name__=='__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('home.html')


# ➕ CREATE
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        date = request.form['date']
        temp = request.form['temperature']
        hum = request.form['humidity']

        new_log = Weather(date=date, temperature=temp, humidity=hum)
        db.session.add(new_log)
        db.session.commit()

        return redirect('/read')

    return render_template('create.html')


# 📖 READ
@app.route('/read')
def read():
    logs = Weather.query.all()
    return render_template('read.html', logs=logs)


# ✏️ UPDATE
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    log = Weather.query.get(id)

    if request.method == 'POST':
        log.date = request.form['date']
        log.temperature = request.form['temperature']
        log.humidity = request.form['humidity']

        db.session.commit()
        return redirect('/read')

    return render_template('update.html', log=log)


# ❌ DELETE
@app.route('/delete/<int:id>')
def delete(id):
    log = Weather.query.get(id)
    db.session.delete(log)
    db.session.commit()
    return redirect('/read')


# Run app
if __name__ == '__main__':
    app.run(debug=True)