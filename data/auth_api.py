from flask import Blueprint, render_template, request, flash

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

    return render_template('login.html')


@auth_page.route('/logout')
def logout():
    return '<h>logout</h>'


@auth_page.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if '@' not in email:
            flash('Некорректный адрес почты', category='error')
        elif len(email) < 3:
            flash('Длина адреса почты должна быть не менее 3 символов', category='error')
        # если почта уже есть в базе
        elif len(password1) < 8:
            flash('Длина пароля должна быть не менее 8 символов', category='error')
        elif len(password1) > 100:
            flash('Длина пароля должна быть менее 100 символов', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают', category='error')
        else:
            flash('Аккаунт создан', category='success')

    #         добавить пользователя
    elif request.method == 'GET':
        pass

    return render_template('signup.html')
