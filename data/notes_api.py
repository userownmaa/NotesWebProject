from flask import Blueprint, render_template


notes_page = Blueprint(
    'notes_api',
    __name__,
    template_folder='templates'
)