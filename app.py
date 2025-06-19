from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///golf.db'  # You’ll use Postgres later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'your-unique-secret-key'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    rounds = db.relationship('Round', backref='user', lazy=True)

user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def __repr__(self):
    return f"<Round {self.course} - {self.score}>"


# In-memory storage of rounds (list of dicts)
rounds = []
next_id = 1

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    user_rounds = Round.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', rounds=user_rounds)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_round():
    if request.method == 'POST':
        new_round = Round(
            date=request.form['date'],
            course=request.form['course'],
            score=request.form['score'],
            notes=request.form.get('notes', ''),
            user=current_user
        )
        db.session.add(new_round)
        db.session.commit()
        return redirect(url_for('index'))
    flash("Round updated successfully!")
    return render_template('add_round.html')
    


@app.route('/edit/<int:round_id>', methods=['GET', 'POST'])
@login_required
def edit_round(round_id):
    round_to_edit = Round.query.get_or_404(round_id)

    if round_to_edit.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == 'POST':
        round_to_edit.date = request.form['date']
        round_to_edit.course = request.form['course']
        round_to_edit.score = request.form['score']
        round_to_edit.notes = request.form.get('notes', '')

        db.session.commit()
        return redirect(url_for('index'))
        
    flash("Round updated successfully!")
    return render_template('edit_round.html', round=round_to_edit)



@app.route('/delete/<int:round_id>', methods=['POST'])
@login_required
def delete_round(round_id):
    round_to_delete = Round.query.get_or_404(round_id)

    if round_to_delete.user_id != current_user.id:
        return "Unauthorized", 403

    db.session.delete(round_to_delete)
    db.session.commit()
    flash("Round updated successfully!")
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
