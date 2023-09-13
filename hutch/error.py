from flask import Blueprint, render_template
from flask_login import login_required, current_user


error = Blueprint('view', __name__)

@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404
