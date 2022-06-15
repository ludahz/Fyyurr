from crypt import methods
from flask import Blueprint

from controllers.ArtistController import artists, create_artist_form, create_artist_submission, edit_artist, edit_artist_submission, search_artists, show_artist


artist_bp = Blueprint('artist_bp', __name__)

# @app.route('/artists')
artist_bp.route('/')(artists)
# @app.route('/artists/search', methods=['POST'])
artist_bp.route('/search', methods=['GET', 'POST'])(search_artists)
# @app.route('/artists/<int:artist_id>')
artist_bp.route('/<int:artist_id>')(show_artist)
# @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
artist_bp.route('/<int:artist_id>/edit', methods=['GET'])(edit_artist)
# @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
artist_bp.route('/<int:artist_id>/edit',
                methods=['POST'])(edit_artist_submission)
# @app.route('/artists/create', methods=['GET'])
artist_bp.route('/create', methods=['GET'])(create_artist_form)
# @app.route('/artists/create', methods=['POST'])
artist_bp.route('/create', methods=['POST'])(create_artist_submission)
