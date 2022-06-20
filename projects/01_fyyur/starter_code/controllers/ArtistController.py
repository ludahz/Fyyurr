import re
import sys
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash
)
from forms import *
from models.Models import (
    Artist,
    Show,
    Venue
)
from manage import db


#  Artists
#  ----------------------------------------------------------------
# @app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = []

    for obj in artists:
        upcoming_shows_query = db.session.query(Show).join(Artist).filter(
            Show.artist_id == obj.id).filter(Show.start_time > datetime.now()).all()
        data.append(
            {
                'id': obj.id,
                'name': obj.name,
                "num_upcoming_shows": len(upcoming_shows_query)
            }
        )
    return render_template('pages/artists.html', artists=data)

#  Update
#  ----------------------------------------------------------------


# @app.route('/artists/search', methods=['POST'])
def search_artists():
    form = SearchFrom()
    search = form.search_term.data
    artists = Artist.query.all()
    response = {}
    data = []
    count = []
    for artist in artists:
        if re.search(str(search).lower(), artist.name.lower()):
            upcoming_shows_query = db.session.query(Show).join(Artist).filter(
                Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).all()
            count.append(artist)

            data.append({
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": len(upcoming_shows_query),
            })
        response['count'] = len(count)
        response['data'] = data

    return render_template('pages/search_artists.html', form=form, results=response, search_term=request.form.get('search_term', ''))


# @app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    past_shows = []
    upcoming_shows = []
    artist_obj_result = Artist.query.get(artist_id)
    past_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()

    for show in past_shows_query:
        venue = Venue.query.get(show.venue_id)
        past_show = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time
        }
        past_shows.append(past_show)
    upcoming_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()

    for show in upcoming_shows_query:
        venue = Venue.query.get(show.venue_id)
        upcoming_show = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time
        }
        upcoming_shows.append(upcoming_show)

    data = vars(artist_obj_result)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows_query)
    data['upcoming_shows_count'] = len(upcoming_shows_query)

    # data = list(filter(lambda d: d['id'] ==
    #             artist_id, [data1, data2, data3]))[0]
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form['name'].data = artist.name
    form['genres'].data = artist.genres
    form['city'].data = artist.city
    form['state'].data = artist.state
    form['phone'].data = artist.phone
    form['website_link'].data = artist.website_link
    form['facebook_link'].data = artist.facebook_link
    form['seeking_venue'].data = artist.seeking_venue
    form['seeking_description'].data = artist.seeking_description
    form['image_link'].data = artist.image_link
    return render_template('forms/edit_artist.html', form=form, artist=artist)


# @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)

    if request.method == 'POST':
        artist.name = form['name'].data
        artist.city = form['city'].data
        artist.state = form['state'].data
        artist.phone = form['phone'].data
        artist.genres = form['genres'].data
        artist.facebook_link = form['facebook_link'].data
        artist.image_link = form['image_link'].data
        artist.website_link = form['website_link'].data
        artist.seeking_venue = form['seeking_venue'].data
        artist.seeking_description = form['seeking_description'].data
        try:
            db.session.commit()
            flash('Artist ' + form['name'].data + ' was successfully updated!')

        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Artist ' +
                  form['name'].data + ' could not be updated.')

        finally:
            db.session.close()

    return redirect(url_for('artist_bp.show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------


# @app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


# @app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm()
    if form.validate():
        artist = Artist(
            name=form['name'].data,
            city=form['city'].data,
            state=form['state'].data,
            phone=form['phone'].data,
            genres=form['genres'].data,
            facebook_link=form['facebook_link'].data,
            image_link=form['image_link'].data,
            website_link=form['website_link'].data,
            seeking_venue=form['seeking_venue'].data,
            seeking_description=form['seeking_description'].data
        )
        try:
            db.session.add(artist)
            db.session.commit()
            flash('Artist ' + form['name'].data + ' was successfully listed!')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Artist ' +
                  form['name'].data + ' could not be listed.')
    else:
        return render_template('forms/new_artist.html', form=form)
    return render_template('pages/home.html')
