from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage of rounds (list of dicts)
rounds = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html', rounds=rounds)

@app.route('/add', methods=['GET', 'POST'])
def add_round():
    global next_id
    if request.method == 'POST':
        round_data = {
            'id': next_id,
            'date': request.form['date'],
            'course': request.form['course'],
            'score': request.form['score'],
            'notes': request.form.get('notes', '')
        }
        rounds.append(round_data)
        next_id += 1
        return redirect(url_for('index'))
    return render_template('add_round.html')

@app.route('/edit/<int:round_id>', methods=['GET', 'POST'])
def edit_round(round_id):
    round_to_edit = next((r for r in rounds if r['id'] == round_id), None)
    if not round_to_edit:
        return 'Round not found', 404
    if request.method == 'POST':
        round_to_edit['date'] = request.form['date']
        round_to_edit['course'] = request.form['course']
        round_to_edit['score'] = request.form['score']
        round_to_edit['notes'] = request.form.get('notes', '')
        return redirect(url_for('index'))
    return render_template('edit_round.html', round=round_to_edit)

@app.route('/delete/<int:round_id>', methods=['POST'])
def delete_round(round_id):
    global rounds
    rounds = [r for r in rounds if r['id'] != round_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
