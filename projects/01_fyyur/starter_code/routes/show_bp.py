from flask import Blueprint

from controllers.ShowController import (
    create_show_submission,
    create_shows,
    shows
)

show_bp = Blueprint('show_bp', __name__)

# @app.route('/shows')
show_bp.route('/')(shows)
# @app.route('/shows/create')
show_bp.route('/create')(create_shows)
# @app.route('/shows/create', methods=['POST'])
show_bp.route('/create', methods=['POST'])(create_show_submission)
