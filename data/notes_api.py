from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from data import db_session
from data.groups import Group
from data.notes import Note

notes_page = Blueprint(
    'notes_api',
    __name__,
    template_folder='templates'
)


@notes_page.route('/', methods=['GET', 'POST'])
def home_page():
    if current_user.is_authenticated:
        return redirect('/notes')
    else:
        return redirect(url_for('auth_api.login'))


@notes_page.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    db_sess = db_session.create_session()
    cur_notes = db_sess.query(Note).filter((Note.user == current_user), (Note.group_id == 0)).order_by(Note.date.desc())
    cur_groups = db_sess.query(Group).filter(Group.user == current_user).order_by(Group.date.desc())

    if request.method == 'POST':
        search_group = request.form.get('search_group')
        search_note = request.form.get('search_note')
        if search_group:
            new_groups = []
            for item in cur_groups:
                if search_group.lower() in item.title.lower() or search_group.lower() in item.content.lower():
                    new_groups.append(item)
            cur_groups = new_groups
        elif search_note:
            new_notes = []
            for item in cur_notes:
                if search_note.lower() in item.content.lower() or search_note.lower() in item.title.lower():
                    new_notes.append(item)
            cur_notes = new_notes
    return render_template('notes.html', user=current_user, notes=cur_notes, groups=cur_groups)


@notes_page.route('/group/<int:id>', methods=['GET', 'POST'])
def group(id):
    db_sess = db_session.create_session()
    cur_notes = db_sess.query(Note).filter((Note.user == current_user), (Note.group_id == id)).order_by(Note.date.desc())
    cur_group = db_sess.query(Group).get(id)

    if request.method == 'POST':
        search = request.form.get('search')
        if search:
            new_notes = []
            for item in cur_notes:
                if search.lower() in item.content.lower() or search.lower() in item.title.lower():
                    new_notes.append(item)
            cur_notes = new_notes
    return render_template('group.html', user=current_user, notes=cur_notes, group=cur_group)


@notes_page.route('/create/note', methods=['GET', 'POST'])
def create_note():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        title = request.form.get('title')
        note = request.form.get('note')
        if title and note:
            new_note = Note(user_id=current_user.id, title=title, content=note)
            db_sess.add(new_note)
            db_sess.commit()
            flash('Заметка создана.', category='success')
            return redirect('/notes')

        else:
            flash('Пустое поле.', category='error')
            return render_template('create_note.html', user=current_user)
    else:
        return render_template('create_note.html', user=current_user)


@notes_page.route('/create/group', methods=['GET', 'POST'])
def create_group():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title:
            new_group = Group(user_id=current_user.id, title=title, content=description)
            db_sess.add(new_group)
            db_sess.commit()
            flash('Группа создана.', category='success')
            return redirect('/notes')

        else:
            flash('Пустое поле.', category='error')
            return render_template('create_group.html', user=current_user)
    else:
        return render_template('create_group.html', user=current_user)


@notes_page.route('/add-to-group/<int:group_id>/<int:note_id>', methods=['GET', 'POST'])
def add_note_to_group(group_id, note_id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(note_id)
    note.group_id = group_id
    db_sess.commit()
    flash('Заметка добавлена.', category='success')
    return redirect('/notes')


@notes_page.route('/delete-from-group/<int:group_id>/<int:note_id>', methods=['GET', 'POST'])
def delete_note_from_group(group_id, note_id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(note_id)
    note.group_id = 0
    db_sess.commit()
    flash('Заметка удалена из группы.', category='success')
    return redirect(f'/group/{group_id}')


@notes_page.route('/delete/note/<int:id>', methods=['GET', 'POST'])
def delete_note(id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(id)

    if note:
        db_sess.delete(note)
        db_sess.commit()
    flash('Заметка удалена.', category='success')
    if note.group_id == 0:
        return redirect('/notes')
    else:
        return redirect(f'/group/{note.group_id}')


@notes_page.route('/delete/group/<int:id>', methods=['GET', 'POST'])
def delete_group(id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).get(id)
    if group:
        db_sess.delete(group)
        db_sess.commit()
    flash('Группа удалена.', category='success')
    return redirect('/notes')


@notes_page.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(id)

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('note')
        db_sess.commit()
        flash('Заметка изменена.', category='success')
        if note.group_id == 0:
            return redirect('/notes')
        else:
            return redirect(f'/group/{note.group_id}')
    else:
        return render_template('edit.html', user=current_user, note=note)
