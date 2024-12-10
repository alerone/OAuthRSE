from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.todo_crud import create_todo

todo_bp = Blueprint('todo', __name__)

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
    
    return render_template('create_todo.html')
