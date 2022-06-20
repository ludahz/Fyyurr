from flask import Blueprint
from controllers.VenuesController import (
    create_venue_form,
    create_venue_submission,
    delete_venue, edit_venue,
    edit_venue_submission,
    search_venues,
    show_venue,
    venues
)

venue_bp = Blueprint('venue_bp', __name__)

# @app.route('/venues')
venue_bp.route('/')(venues)
# @app.route('/venues/create', methods=['GET'])
venue_bp.route('/create', methods=['GET'])(create_venue_form)
# @app.route('/venues/create', methods=['POST'])
venue_bp.route('/create', methods=['POST'])(create_venue_submission)
# @app.route('/venues/<int:venue_id>')
venue_bp.route('/<int:venue_id>')(show_venue)
# @app.route('/venues/<venue_id>/delete', methods=['DELETE'])
venue_bp.route('/<int:venue_id>/delete', methods=['GET'])(delete_venue)
# @app.route('/venues/<venue_id>/delete', methods=['DELETE'])
venue_bp.route('/<int:venue_id>/delete', methods=['DELETE'])(delete_venue)
# @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
venue_bp.route('/<int:venue_id>/edit', methods=['GET'])(edit_venue)
# @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
venue_bp.route('/<int:venue_id>/edit',
               methods=['POST'])(edit_venue_submission)
# @app.route('/venues/search', methods=['POST'])
venue_bp.route('/search', methods=['GET', 'POST'])(search_venues)
