import sqlite3
import os

from flask import Flask, render_template, url_for, request, g, flash

from FDataBase import FDataBase


DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'ajsdhfgkasjdhfgkj3jh42h3j4ggbghvgb023'


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
    

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [{"name": "Главная", "url": "index"}, 
        {"name": "Номера", "url": "rooms"}, 
        {"name": "Услуги", "url": "services"}, 
        {"name": "Отзывы", "url": "reviews"}, 
        {"name": "Контакты", "url": "contact"}, 
        {"name": "О нас", "url": "about"},]


@app.route("/index")
@app.route("/")
def index():
    print( url_for('index') )
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', title = "Главная страница", menu = menu)

@app.route("/rooms")
def rooms():
    print( url_for('rooms') )
    return render_template('rooms.html', title = "Номера", menu = menu)

@app.route("/services")
def services():
    print( url_for('services') )
    return render_template('services.html', title = "Услуги", menu = menu)



@app.route("/reviews", methods=["POST", "GET"])
def reviews():
    print( url_for('reviews') )
    db = get_db()
    dbase = FDataBase(db)
    
    if request.method == 'POST':
        if len(request.form['name']) > 3 and len(request.form['message']) >10:
            res = dbase.addReviews(request.form['name'], request.form['email'], request.form['message'])
            if not res:
                flash('Invalid add reviews', category = 'error')
            else:
                flash('Reviews add', category = 'success')
        else:
            flash('Invalid add reviews')
    
    return render_template('reviews.html', title = "Отзывы", menu = menu, reviews=dbase.getReviewsAnonce())



# @app.route("/reviews/<int:id_reviews>")
# def showReviews(id_reviews):
#     db = get_db()
#     dbase = FDataBase(db)
#     name, message, time = dbase.getReviews(id_reviews)
#     if not name:
#         print("Page not found")
        
#     return render_template('show_reviews.html', title = "Отзыв", menu = menu, name=name, message=message, time=time)


@app.route("/contact")
def contact():
    print( url_for('contact') )
    return render_template('contact.html', title = "Контакты", menu = menu)

@app.route("/about")
def about():
    print( url_for('about') )
    return render_template('about.html', title = "О нас", menu = menu)

@app.route("/rent-rooms")
def rent():
    print( url_for('rent') )
    return render_template('rent-rooms.html', title = "Забронировать номер", menu = menu)



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()



if __name__ == "__main__":
    app.run(debug=True)