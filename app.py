from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dates.db'
db = SQLAlchemy(app)

class DateRange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat()
        }

with app.app_context():
    # db.drop_all()
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        date_range = DateRange(name=name, start_date=start_date, end_date=end_date)
        db.session.add(date_range)
        db.session.commit()
    date_ranges = [dr.to_dict() for dr in DateRange.query.all()]
    return render_template('index.html', date_ranges=date_ranges)

if __name__ == '__main__':
    app.run(debug=True)