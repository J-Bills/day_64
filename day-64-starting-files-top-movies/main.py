from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,
from wtforms.validators import DataRequired
import requests

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


class EditMovie(FlaskForm):
    rating = StringField('What is your rating out of 10?', validators=[DataRequired()])
    review = StringField('What is your review?', validators=[DataRequired()])
    submit = SubmitField('Done')

class DeleteMovie(FlaskForm):
    question
    submit = SubmitField('Done')


@app.route("/<id>")
def home(id):
    result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
    all_movies = result.scalars().all()
    count = int(id) - 1
    movie = all_movies[count]
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
            # id = int(movie_id) - 1
        return redirect(url_for('home', id=movie_id))
    movie_id = id
    updated_movie = db.get_or_404(Movie, movie_id)
    return render_template("edit.html", movie=updated_movie, form=update_form)
@app.route("/delete")
def delete_movie():
    delete_form = DeleteMovie()
    if request.method == 'POST' and delete_form.validate_on_submit():
        with app.app_context():
            movie_id = id
            rating = delete_form.rating.data
            review = delete_form.review.data
            updated_movie = db.get_or_404(Movie, movie_id)
            updated_movie.rating = rating
            updated_movie.review = review
            db.session.commit()
            # id = int(movie_id) - 1
        return redirect(url_for('home', id=movie_id))
    movie_id = id
    updated_movie = db.get_or_404(Movie, movie_id)
    return render_template("edit.html", movie=updated_movie, form=delete_form)

    return render_template("delete.html", all_movies=all_movies)
@app.route("/add")
def add_movie():
    result = db.session.execute(db.select(Movie).order_by(Movie.title))
    all_movies = result.scalars().all()

    return render_template("add.html", all_movies=all_movies)




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
