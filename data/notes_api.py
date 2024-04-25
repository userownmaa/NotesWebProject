from flask import Blueprint, render_template, request, flash, redirect
from flask_login import current_user

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
    cur_notes = db_sess.query(Note).filter(Note.user == current_user)

    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        search = request.form.get('search')
        # if search:
        #     all_notes = db_sess.query(Note).filter(Note.user == current_user)
        #     for item in all_notes:
        #         if search in item.content:
        #             cur_notes.append(item)
        if title and note:
            new_note = Note(user_id=current_user.id, title=title, content=note)
            db_sess.add(new_note)
            db_sess.commit()
            flash('Заметка добавлена.', category='success')
            cur_notes = db_sess.query(Note).filter(Note.user == current_user)
        else:
            pass
            # flash('Пустое поле.', category='error')

    return render_template('notes.html', user=current_user, notes=cur_notes)


@notes_page.route('/add/<int:id>', methods=['GET', 'POST'])
def add():
    pass


@notes_page.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(id)
    if note:
        db_sess.delete(note)
        db_sess.commit()
    return redirect('/notes')


@notes_page.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(id)

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('note')
        db_sess.commit()
        return redirect('/notes')
    else:
        return render_template('edit.html', user=current_user, note=note)


