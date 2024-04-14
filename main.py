from flask import Flask
from data import db_session, notes_api, auth_api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(notes_api.notes_page, url_prefix='/')
    app.register_blueprint(auth_api.auth_page, url_prefix='/')
    app.run(debug=True)


if __name__ == '__main__':
    main()
