from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user


notes_page = Blueprint(
    'notes_api',
    __name__,
    template_folder='templates'
)


@notes_page.route('/')
@login_required
def notes():
    return render_template('notes.html', user=current_user)

