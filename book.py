from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# SQLite database file path
db_file_path = os.path.join(os.path.dirname(__file__), 'book.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    book_title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Book {self.username}>'

# Create all tables if they do not exist
with app.app_context():
    db.create_all()

# Route to render the form
@app.route('/')
def booking_form():
    return render_template('book.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_booking():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        book_title = request.form['book-title']
        author = request.form['author']
        borrow_date = datetime.strptime(request.form['borrow-date'], '%Y-%m-%d').date()
        return_date = datetime.strptime(request.form['return-date'], '%Y-%m-%d').date()

        # Create a new Book object
        new_booking = Book(username=username, email=email, phone=phone, book_title=book_title, author=author,
                           borrow_date=borrow_date, return_date=return_date)

        # Add the new booking to the database session
        db.session.add(new_booking)
        db.session.commit()

        # Redirect to the confirmation page
        return redirect(url_for('confirmation'))

# Route to display confirmation page
@app.route('/confirmation')
def confirmation():
    return render_template('confirm.html')

if __name__ == '__main__':
    app.run(debug=True)
