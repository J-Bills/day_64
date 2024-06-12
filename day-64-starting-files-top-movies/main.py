from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from os import environ

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer(), nullable=False)
    description: Mapped[str] = mapped_column(String(80))
    rating: Mapped[float] = mapped_column(Float(), nullable=False)
    ranking: Mapped[int] = mapped_column(Integer(), nullable=False)
    review: Mapped[str] = mapped_column(String(30))
    img_url: Mapped[str] = mapped_column(String(30))



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6c'
Bootstrap5(app)

class SearchMovie():
    api_key = environ.get('MOVIE_API_KEY')
    api_rac = environ.get('MOVIE_API_RAC')
    def __init__(self):
        
        pass

class EditMovie(FlaskForm):
    rating = StringField('What is your rating out of 10?', validators=[DataRequired()])
    review = StringField('What is your review?', validators=[DataRequired()])
    submit = SubmitField('Done')


class DeleteMovie(FlaskForm):
    back = SubmitField('Back')
    delete = SubmitField('Delete')

class AddMovie(FlaskForm):
    movie_title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Add')


@app.route('/')
def index():
    all_movies = Movie.query.order_by(desc(Movie.ranking)).all()
    movie = all_movies[0]
    return render_template("index.html", movie=movie)


@app.route("/<id>")
def home(id):
    all_movies = Movie.query.order_by(desc(Movie.ranking)).all()
    count = int(id) - 1
    movie = all_movies[count]
    print(movie.title)
    return render_template("index.html", movie=movie)


@app.route("/edit/<id>", methods=['GET', 'POST'])
def update_movie(id):
    update_form = EditMovie()
    if request.method == 'POST' and update_form.validate_on_submit():
        with app.app_context():
            movie_id = id
            rating = update_form.rating.data
            review = update_form.review.data
            updated_movie = db.get_or_404(Movie, movie_id)
            updated_movie.rating = rating
            updated_movie.review = review
            db.session.commit()
        return redirect(url_for('home', id=movie_id))
    movie_id = id
    updated_movie = db.get_or_404(Movie, movie_id)
    return render_template("edit.html", movie=updated_movie, form=update_form)


@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete_movie(id):
    delete_form = DeleteMovie()
    movie_id = id
    if request.method == 'POST' and delete_form.validate_on_submit() and delete_form.delete.data:
        with app.app_context():
            movie_to_delete = db.get_or_404(Movie, movie_id)
            db.session.delete(movie_to_delete)
            db.session.commit()
        return redirect(url_for('index'))

    elif delete_form.back.data:
        return redirect(url_for('home', id=movie_id))

    movie_to_delete = db.get_or_404(Movie, movie_id)
    return render_template("delete.html", movie=movie_to_delete, form=delete_form)


@app.route("/add", methods=['GET', 'POST'])
def add_movie():
    add_form = AddMovie()
    if request.method == "POST" and add_form.validate_on_submit():
        with app.app_context():
            movie_title = add_form.movie_title.data
            db.session.add(Movie(title=movie_title))
            db.session.commit()


    return render_template("add.html")




if __name__ == '__main__':
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-ten-movies-collection.db"
    # initialize the app with the extension
    db.init_app(app)
    with app.app_context():
        second_movie = Movie(
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=7.3,
            ranking=9,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
        )
        # db.session.add(second_movie)
        # db.session.commit()
        db.create_all()

    app.run(debug=True)
