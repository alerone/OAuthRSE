from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.todo_crud import create_todo, get_todo_by_id, delete_todo

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todo_info/<int:todo_id>', methods=['GET'])
def info(todo_id: int):

    if 'user' not in session:
        flash("Debes iniciar sesión para crear una tarea", 'error')
        return redirect(url_for('auth.login'))
    todo = get_todo_by_id(todo_id)

    if not todo:
        flash('La tarea no existe.', 'error')
        return redirect(url_for('home'))

    return render_template('create_todo.html', todo=todo)

@todo_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        flash("Debes iniciar sesión para crear una tarea", 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('El nombre es obligatorio', 'error')
            return render_template('create_todo.html')
        print("created by", session['user']['id'])
        
        create_todo(name=name, description=description, created_by=session['user']['id'])
        flash('Tarea creada con éxito!', 'success')
        return redirect(url_for('todo.create'))
    
    return render_template('create_todo.html', todo=None)

@todo_bp.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id: int):
    if 'user' not in session:
        flash("Debes iniciar sesión para crear una tarea", 'error')
        return redirect(url_for('auth.login'))
    todo = get_todo_by_id(todo_id)

    if not todo:
        flash('La tarea no existe.', 'error')
        return redirect(url_for('home'))
    
    if todo.created_by != session['user']['id']:
        flash('No tienes permiso para borrar esta tarea.', 'error')
        return redirect(url_for('home'))
    if delete_todo(todo):
        flash('Tarea eliminada con éxito.', 'success')
    else:
        flash('Error al intentar eliminar la tarea.', 'error')
        
    return redirect(url_for('home'))
