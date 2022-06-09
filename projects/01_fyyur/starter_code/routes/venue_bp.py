from flask import Blueprint
from controllers.VenuesController import create_venue_form, create_venue_submission, delete_venue, venues

venue_bp = Blueprint('venue_bp', __name__)

# @app.route('/venues')
venue_bp.route('/')(venues)
# @app.route('/venues/create', methods=['GET'])
venue_bp.route('/create', methods=['GET'])(create_venue_form)
# @app.route('/venues/create', methods=['POST'])
venue_bp.route('/create', methods=['POST'])(create_venue_submission)
# @app.route('/venues/<venue_id>', methods=['DELETE'])
venue_bp.route('/<venue_id>', methods=['DELETE'])(delete_venue)