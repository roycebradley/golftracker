from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///golf.db'  # You’ll use Postgres later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

def __repr__(self):
    return f"<Round {self.course} - {self.score}>"


# In-memory storage of rounds (list of dicts)
rounds = []
next_id = 1

@app.route('/')
def index():
    all_rounds = Round.query.all()
    return render_template('index.html', rounds=all_rounds)

@app.route('/add', methods=['GET', 'POST'])
def add_round():
    if request.method == 'POST':
        new_round = Round(
            date=request.form['date'],
            course=request.form['course'],
            score=request.form['score'],
            notes=request.form.get('notes', '')
        )
        db.session.add(new_round)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_round.html')


@app.route('/edit/<int:round_id>', methods=['GET', 'POST'])
def edit_round(round_id):
    round_to_edit = Round.query.get_or_404(round_id)

    if request.method == 'POST':
        round_to_edit.date = request.form['date']
        round_to_edit.course = request.form['course']
        round_to_edit.score = request.form['score']
        round_to_edit.notes = request.form.get('notes', '')
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_round.html', round=round_to_edit)


@app.route('/delete/<int:round_id>', methods=['POST'])
def delete_round(round_id):
    round_to_delete = Round.query.get_or_404(round_id)
    db.session.delete(round_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
