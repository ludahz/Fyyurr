import re
import sys
from flask import render_template, redirect, url_for, request, abort, flash
from forms import *
from models.Models import Artist, Show, Venue
from manage import db


#  Artists
#  ----------------------------------------------------------------
# @app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []
    for obj in artists:
        data.append(
            {
                'id': obj.id,
                'name': obj.name
            }
        )
    return render_template('pages/artists.html', artists=data)


# @app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    form = SearchFrom()
    search = form.search_term.data
    artists = Artist.query.all()
    response = {}
    data = []
    count = []
    count_shows = []

    for artist in artists:
        if re.search(str(search).lower(), artist.name.lower()):
            shows = Show.query.filter_by(artist_id=artist.id)
            for show in shows:
                if show.start_time > datetime.now():
                    count_shows.append(show)
                else:
                    pass
                count.append(artist)
                response['count'] = len(count)
                data.append({
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": len(count_shows),
                })
                response['data'] = data
                count_shows = []

    return render_template('pages/search_artists.html', form=form, results=response, search_term=request.form.get('search_term', ''))


# @app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    artist_obj_result = Artist.query.get(artist_id)
    count_upcoming = []
    count_past = []
    upcoming_shows = []
    upcoming_show = []
    past_show = []
    past_shows = []
    shows = Show.query.filter_by(artist_id=artist_id)
    for show in shows:
        venue = Venue.query.get(show.venue_id)
        if show.start_time > datetime.now():
            count_upcoming.append(show)
            upcoming_show = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            }
            upcoming_shows.append(upcoming_show)
        else:
            count_past.append(show)
            past_show = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time
            }
            past_shows.append(past_show)

    data = vars(artist_obj_result)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(count_past)
    data['upcoming_shows_count'] = len(count_upcoming)

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
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


# @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
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
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm()
    error = False
    print(form['name'].data)
    try:
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
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + form['name'].data + ' was successfully listed!')
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' +
              form['name'].data + ' could not be listed.')
    finally:
        db.session.close()
    if error:
        print('Error!!!')
    else:
        print('All good')

    return render_template('pages/home.html')
