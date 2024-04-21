from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from werkzeug.security import generate_password_hash, check_password_hash


auth_page = Blueprint(
    'auth_api',
    __name__,
    template_folder='templates'
)


@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db_sess.query(User).filter(User.email == email).first()
        if user:
            if check_password_hash(user.hashed_password, password):
                flash('Вход выполнен.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('notes_api.notes'))
            else:
                flash('Неправильный пароль.', category='error')
        else:
            flash('Пользователья с данным адресом почты не существует.', category='error')

    return render_template('login.html', user=current_user)


@auth_page.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_api.login'))


@auth_page.route('/signup', methods=['GET', 'POST'])
def signup():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = db_sess.query(User).filter(User.email == email).first()
        if user:
            flash('Пользователь с данным адресом почты уже существует.', category='error')
        elif '@' not in email:
            flash('Некорректный адрес почты.', category='error')
        elif len(email) < 3:
            flash('Длина адреса почты должна быть не менее 3 символов.', category='error')
        elif len(password1) < 8:
            flash('Длина пароля должна быть не менее 8 символов.', category='error')
        elif len(password1) > 100:
            flash('Длина пароля должна быть менее 100 символов.', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают.', category='error')
        else:
            user = User(email=email, first_name=first_name, second_name=second_name,
                        hashed_password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db_sess.add(user)
            db_sess.commit()
            flash('Аккаунт создан.', category='success')
            login_user(user, remember=True)
            return redirect(url_for('notes_api.notes'))

    return render_template('signup.html', user=current_user)
