import sys
from flask import (
    render_template,
    flash
)
from forms import *
from models.Models import (
    Artist,
    Show,
    Venue
)
from manage import db

#  Shows
#  ----------------------------------------------------------------
# @app.route('/shows')


def shows():
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
    form = ShowForm()
    try:
        show = Show(
            venue_id=form['venue_id'].data,
            artist_id=form['artist_id'].data,
            start_time=form['start_time'].data
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')
