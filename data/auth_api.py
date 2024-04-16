from flask import Blueprint, render_template

auth_page = Blueprint(
    'auth_api',
    __name__,
    template_folder='templates'
)


@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #
    # elif request.method == 'GET':

    return '<h>login</h>'


@auth_page.route('/logout')
def logout():
    return '<h>logout</h>'


@auth_page.route('/signup', methods=['GET', 'POST'])
def sign_up():
    # if request.method == 'POST':
    #
    # elif request.method == 'GET':

    return '<h>signup</h>'
