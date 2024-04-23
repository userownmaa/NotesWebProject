from flask import Flask
from flask_restful import Api

from data import db_session, notes_api, auth_api, resources
from flask_login import LoginManager
from data.users import User


app = Flask(__name__)
# api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(int(id))


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(notes_api.notes_page, url_prefix='/')
    app.register_blueprint(auth_api.auth_page, url_prefix='/')
    # api.add_resource(resources.NotesListResource, '/notes')
    # api.add_resource(resources.NotesResource, '/notes/<int:id>')
    app.run(debug=True)


if __name__ == '__main__':
    main()
