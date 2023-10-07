from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlShortnerDatabase.db'
db = SQLAlchemy(app)

class ShortnerTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    original_url = db.Column(db.String(200),nullable=False)
    shortened_url = db.Column(db.String(200),nullable=False)
    created_date_time = db.Column(db.DateTime, default = datetime.utcnow)

@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        original_url = request.form['originalURL']
        shortened_url = 'https://umasankar.shorten/' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(7))
        new_shortened_data = ShortnerTable(original_url=original_url,shortened_url = shortened_url)
        
        try:
            db.session.add(new_shortened_data)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        shortened_urls = ShortnerTable.query.order_by(ShortnerTable.created_date_time).all()
        return render_template('index.html', shortened_urls = shortened_urls)

@app.route('/getOriginalUrl', methods=['POST'])
def getOriginalUrl():
    try:
        shortened_url = request.form['shortenedURL']
        return ShortnerTable.query.filter_by(shortened_url=shortened_url).first().original_url
    except:
        return 'Shortened URL not valid'

if __name__ == "__main__":
    app.run(debug = True)