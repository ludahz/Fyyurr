import sys
from flask import render_template, redirect, url_for, request, abort, flash
from forms import *
from models.Models import Artist, Show, Venue
from manage import db

#  Shows
#  ----------------------------------------------------------------
# @app.route('/shows')


def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    dataList = Show.query.all()
    show_data = []
    data = []
    for obj in dataList:
        venue = Venue.query.get(obj.venue_id)
        artist = Artist.query.get(obj.artist_id)
        show_data = {
            "venue_id": obj.venue_id,
            "venue_name": venue.name,
            "artist_id": obj.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": obj.start_time
        }
        data.append(show_data)
    return render_template('pages/shows.html', shows=data)


# @app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


# @app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm()
    try:
        show = Show(
            venue_id=form['venue_id'].data,
            artist_id=form['artist_id'].data,
            start_time=form['start_time'].data
        )
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
