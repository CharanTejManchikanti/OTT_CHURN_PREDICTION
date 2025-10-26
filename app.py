from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load ML model
model = joblib.load("xgmodel.pkl")

# ---------- DATABASE CONFIG ----------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'predictions': 'sqlite:///predictions.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- MODELS ----------
# User Login Info - stored in users.db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# User Predictions - stored in predictions.db
class UserInput(db.Model):
    __bind_key__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    no_of_days_subscribed = db.Column(db.Integer, nullable=False)
    multi_screen = db.Column(db.String(5), nullable=False)
    mail_subscribed = db.Column(db.String(5), nullable=False)
    weekly_mins_watched = db.Column(db.Integer, nullable=False)
    minimum_daily_mins = db.Column(db.Integer, nullable=False)
    maximum_daily_mins = db.Column(db.Integer, nullable=False)
    weekly_max_night_mins = db.Column(db.Integer, nullable=False)
    videos_watched = db.Column(db.Integer, nullable=False)
    maximum_days_inactive = db.Column(db.Integer, nullable=False)
    customer_support_calls = db.Column(db.Integer, nullable=False)
    prediction = db.Column(db.String(20), nullable=False)

# ---------- CREATE TABLES ----------
with app.app_context():
    db.create_all()

# ---------- ROUTES ----------
@app.route('/')
def home():
    return render_template('base.html', username=session.get('user'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="User already exists!")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.add(User(username=username, password=hashed_password))
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect('/dashboard')
        return render_template('login.html', error="Invalid username or password!")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    recent_predictions = UserInput.query.filter_by(username=session['user'])\
                                        .order_by(UserInput.id.desc())\
                                        .limit(5)\
                                        .all()

    return render_template('dashboard.html', username=session['user'], predictions=recent_predictions)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            user_data = {
                'age': int(request.form['age']),
                'no_of_days_subscribed': int(request.form['no_of_days_subscribed']),
                'weekly_mins_watched': int(request.form['weekly_mins_watched']),
                'minimum_daily_mins': int(request.form['minimum_daily_mins']),
                'maximum_daily_mins': int(request.form['maximum_daily_mins']),
                'weekly_max_night_mins': int(request.form['weekly_max_night_mins']),
                'videos_watched': int(request.form['videos_watched']),
                'maximum_days_inactive': int(request.form['maximum_days_inactive']),
                'customer_support_calls': int(request.form['customer_support_calls']),
                'gender': request.form['gender'],
                'multi_screen': request.form['multi_screen'],
                'mail_subscribed': request.form['mail_subscribed']
            }

            # Risk Classification
            if (
                user_data['no_of_days_subscribed'] <= 30 or
                user_data['weekly_mins_watched'] < 50 or
                user_data['maximum_days_inactive'] > 20 or
                user_data['customer_support_calls'] > 3 or
                user_data['videos_watched'] < 5 or
                (user_data['no_of_days_subscribed'] > 365 and user_data['weekly_mins_watched'] == 0)
            ):
                result = "Leaving - High Churn Risk"

            elif (
                30 <= user_data['no_of_days_subscribed'] <= 90 or
                50 <= user_data['weekly_mins_watched'] <= 120 or
                5 <= user_data['videos_watched'] <= 10 or
                1 <= user_data['customer_support_calls'] <= 2 or
                10 <= user_data['maximum_days_inactive'] <= 20
            ):
                result = "Medium Churn Risk"

            elif (
                user_data['no_of_days_subscribed'] > 180 and
                user_data['weekly_mins_watched'] > 150 and
                user_data['videos_watched'] > 15 and
                user_data['maximum_days_inactive'] <= 7 and
                user_data['customer_support_calls'] == 0 and
                user_data['minimum_daily_mins'] >= 30 and
                user_data['maximum_daily_mins'] < 300 and
                user_data['weekly_max_night_mins'] < 100 and
                user_data['multi_screen'] == 'yes' and
                user_data['mail_subscribed'] == 'yes'
            ):
                result = "Not Leaving - Low Churn Risk"

            else:
                result = "Medium Churn Risk"

            new_entry = UserInput(
                username=session['user'],
                gender=user_data['gender'],
                age=user_data['age'],
                no_of_days_subscribed=user_data['no_of_days_subscribed'],
                multi_screen=user_data['multi_screen'],
                mail_subscribed=user_data['mail_subscribed'],
                weekly_mins_watched=user_data['weekly_mins_watched'],
                minimum_daily_mins=user_data['minimum_daily_mins'],
                maximum_daily_mins=user_data['maximum_daily_mins'],
                weekly_max_night_mins=user_data['weekly_max_night_mins'],
                videos_watched=user_data['videos_watched'],
                maximum_days_inactive=user_data['maximum_days_inactive'],
                customer_support_calls=user_data['customer_support_calls'],
                prediction=result
            )
            db.session.add(new_entry)
            db.session.commit()

            return render_template('index.html', username=session['user'], prediction_text=f"Prediction: {result}")

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template('predict.html', result=None)

# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run(debug=True)
