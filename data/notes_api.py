from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user

from data import db_session
from data.notes import Note

notes_page = Blueprint(
    'notes_api',
    __name__,
    template_folder='templates'
)


@notes_page.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('home_page.html', user=current_user)


@notes_page.route('/notes', methods=['GET', 'POST'])
def notes():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        search = request.form.get('search')
        cur_notes = []
        if search:
            all_notes = db_sess.query(Note).filter(Note.user == current_user)
            for item in all_notes:

                if search in item.content:
                    cur_notes.append(item)
        elif title and note:
            if len(note) < 1 and len(title) < 1:
                flash('Пустое поле.', category='error')
            else:
                new_note = Note(user_id=current_user.id, title=title, content=note)
                db_sess.add(new_note)
                db_sess.commit()
                flash('Заметка добавлена.', category='success')
            cur_notes = db_sess.query(Note).filter(Note.user == current_user)

    return render_template('notes.html', user=current_user, notes=cur_notes)

