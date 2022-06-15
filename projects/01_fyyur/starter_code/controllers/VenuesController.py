import re
import sys
from unicodedata import name
from flask import render_template, redirect, url_for, request, abort, flash
from sqlalchemy import true
from forms import *
from models.Models import Artist, Show, Venue
from manage import db


#  Venues
#  ----------------------------------------------------------------

# @app.route('/venues')


def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    venue_cities = Venue.query.distinct(Venue.city, Venue.state).all()
    data = []
    temp = []
    append_by_city = []
    append_by_venues = []
    count = []
    form = SearchFrom()
    for venue_city in venue_cities:
        temp = {
            'city': venue_city.city,
            'state': venue_city.state,
        }
        venues_results = Venue.query.filter_by(
            city=venue_city.city, state=venue_city.state).all()
        shows = Show.query.filter_by(venue_id=venue_city.id)
        for show in shows:
            if show.start_time > datetime.now():
                count.append(show)
            else:
                pass
        for venues_res in venues_results:
            append_by_city = {
                "id": venues_res.id,
                "name": venues_res.name,
                "num_upcoming_shows": len(count)
            }
            append_by_venues.append(append_by_city)
        temp['venues'] = append_by_venues
        append_by_venues = []
        data.append(temp)
        count = []
    return render_template('pages/venues.html', areas=data, form=form)

#  Create Venue
#  ----------------------------------------------------------------

# @app.route('/venues/create', methods=['GET'])


def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

# @app.route('/venues/create', methods=['POST'])


def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm()
    error = False
    try:
        venue = Venue(
            name=form['name'].data,
            city=form['city'].data,
            state=form['state'].data,
            address=form['address'].data,
            phone=form['phone'].data,
            genres=form['genres'].data,
            facebook_link=form['facebook_link'].data,
            image_link=form['image_link'].data,
            website_link=form['website_link'].data,
            seeking_talent=form['seeking_talent'].data,
            seeking_description=form['seeking_description'].data
        )
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
        db.session.close()
    if error:
        print('Error!!!')
    else:
        print('All good')

    return render_template('pages/home.html')

# @app.route('/venues/<int:venue_id>')


def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue_obj_result = Venue.query.get(venue_id)
    count_past = []
    count_upcoming = []
    upcoming_show = []
    upcoming_shows = []
    past_show = []
    past_shows = []
    shows = Show.query.filter_by(venue_id=venue_id)
    for show in shows:
        artist = Artist.query.get(show.artist_id)
        if show.start_time > datetime.now():
            count_upcoming.append(show)
            upcoming_show = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time
            }
            upcoming_shows.append(upcoming_show)
        else:
            count_past.append(show)
            past_show = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time
            }
            past_shows.append(past_show)

    data = vars(venue_obj_result)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(count_past)
    data['upcoming_shows_count'] = len(count_upcoming)
    # data = list(filter(lambda d: d['id'] ==
    #             venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=data)


#  DELETE Venue
#  ----------------------------------------------------------------


# @app.route('/venues/<venue_id>', methods=['DELETE'])


def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        record_to_delete = Venue.query.get_or_404(venue_id)
        db.session.delete(record_to_delete)
        db.session.commit()
        flash('Venues record ' + record_to_delete.name +
              ' was successfully deleted!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('Venues record ERROR!!' +
              record_to_delete.name + ' was NOT deleted!!!')
    finally:
        db.session.close()
    return render_template('pages/home.html')

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    #  EDIT Venue
    #  ----------------------------------------------------------------
    # @app.route('/venues/<int:venue_id>/edit', methods=['GET'])


def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    # TODO: populate form with values from venue with ID <venue_id>
    form['name'].data = venue.name
    form['city'].data = venue.city
    form['state'].data = venue.state
    form['address'].data = venue.address
    form['phone'].data = venue.phone
    form['genres'].data = venue.genres
    form['facebook_link'].data = venue.facebook_link
    form['image_link'].data = venue.image_link
    form['website_link'].data = venue.website_link
    form['seeking_talent'].data = venue.seeking_talent
    form['seeking_description'].data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


# @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm()
    venue.name = form['name'].data
    venue.city = form['city'].data
    venue.state = form['state'].data
    venue.address = form['address'].data
    venue.phone = form['phone'].data
    venue.genres = form['genres'].data
    venue.facebook_link = form['facebook_link'].data
    venue.image_link = form['image_link'].data
    venue.website_link = form['website_link'].data
    venue.seeking_talent = form['seeking_talent'].data
    venue.seeking_description = form['seeking_description'].data
    try:
        db.session.commit()
        print('Seeking_talent', venue.seeking_talent)
        flash('Venues ' + form['name'].data + ' was successfully updated!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' +
              form['name'].data + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('venue_bp.show_venue', venue_id=venue_id))

#  SEARCH Venue
#  ----------------------------------------------------------------

# @app.route('/venues/search', methods=['POST'])


def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    form = SearchFrom()
    search = form.search_term.data
    venues = Venue.query.all()
    response = {}
    data = []
    count = []
    count_shows = []
    for venue in venues:
        # if str(search).lower() in venue.name.lower():
        # or using regex
        if re.search(str(search).lower(), venue.name.lower()):
            shows = Show.query.filter_by(venue_id=venue.id)
            for show in shows:
                if show.start_time > datetime.now():
                    count_shows.append(show)
            else:
                pass
            count.append(venue)
            response['count'] = len(count)
            data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(count_shows)
            })
            response['data'] = data
            count_shows = []
    return render_template('pages/search_venues.html', form=form, results=response, search_term=request.form.get('search_term', ''))
