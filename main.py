from flask import Flask
from data import db_session, notes_api, auth_api
from flask_login import LoginManager
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():

    db_session.global_init("db/blogs.db")
    app.register_blueprint(notes_api.notes_page, url_prefix='/')
    app.register_blueprint(auth_api.auth_page, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth_api.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(int(id))

    app.run(debug=True)


if __name__ == '__main__':
    main()
