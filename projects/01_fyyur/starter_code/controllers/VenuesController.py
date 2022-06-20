import re
import sys
from urllib import response
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash
)
from sqlalchemy import true
from forms import *
from models.Models import (
    Artist,
    Show,
    Venue
)
from manage import db


#  Venues
#  ----------------------------------------------------------------


# @app.route('/venues')
def venues():
    venue_cities = Venue.query.distinct(Venue.city, Venue.state).all()
    data = []
    temp = []
    append_by_city = []
    append_by_venues = []
    form = SearchFrom()
    for venue_city in venue_cities:
        temp = {
            'city': venue_city.city,
            'state': venue_city.state,
        }
        upcoming_shows_query = db.session.query(Show).join(Venue).filter(
            Show.venue_id == venue_city.id).filter(Show.start_time > datetime.now()).all()
        venues_results = Venue.query.filter_by(
            city=venue_city.city, state=venue_city.state).all()
        for results in venues_results:
            append_by_city = {
                "id": results.id,
                "name": results.name,
                "num_upcoming_shows": len(upcoming_shows_query)
            }
            append_by_venues.append(append_by_city)
            upcoming_shows_query = []
        temp['venues'] = append_by_venues
        append_by_venues = []
        data.append(temp)
    return render_template('pages/venues.html', areas=data, form=form)

#  Create Venue
#  ----------------------------------------------------------------


# @app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


# @app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    error = False
    if form.validate():
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
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Venue ' +
                  request.form['name'] + ' could not be listed.')
        finally:
            db.session.close()
    else:
        print(form.errors.items())
        return render_template('forms/new_venue.html', form=form)

    return render_template('pages/home.html')


# @app.route('/venues/<int:venue_id>')


def show_venue(venue_id):
    venue_obj_result = Venue.query.get(venue_id)
    upcoming_shows = []
    past_shows = []
    upcoming_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
    for query in upcoming_shows_query:
        artist = Artist.query.get(query.artist_id)
        upcoming_shows.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": query.start_time
        })

    past_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
    for query in past_shows_query:
        artist = Artist.query.get(query.artist_id)
        past_shows.append({
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": query.start_time
        })

    data = vars(venue_obj_result)
    data['past_shows'] = past_shows
    data['upcoming_shows'] = upcoming_shows
    data['past_shows_count'] = len(past_shows_query)
    data['upcoming_shows_count'] = len(upcoming_shows_query)
    # data = list(filter(lambda d: d['id'] ==
    #             venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=data)


#  DELETE Venue
#  ----------------------------------------------------------------


# @app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
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

#  EDIT Venue
#  ----------------------------------------------------------------


# @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
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
    form = SearchFrom()
    search = form.search_term.data
    venues = Venue.query.all()
    response = {}
    data = []
    for venue in venues:
        if re.search(str(search).lower(), venue.name.lower()):
            upcoming_shows_query = db.session.query(Show).join(Venue).filter(
                Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all()
            data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(upcoming_shows_query),
            })
        response['count'] = len(data)
        response['data'] = data
    return render_template('pages/search_venues.html', form=form, results=response, search_term=request.form.get('search_term', ''))
