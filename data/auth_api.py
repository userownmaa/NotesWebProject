from flask import Blueprint, render_template

auth_page = Blueprint(
    'auth_api',
    __name__,
    template_folder='templates'
)