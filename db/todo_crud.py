from .models import ToDo
from .database import SessionLocal 
from sqlalchemy.orm import joinedload

def create_todo(name: str, description: str, created_by: int, photo_id: str):
    db = SessionLocal()
    try:
        new_todo = ToDo(name=name, description=description, created_by=created_by, photo_id=photo_id)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    
    except Exception as e:
        db.rollback()
        print("Error al crear la To Do:", e)
    
    finally:
        db.close()

def delete_todo(todo: ToDo):
    with SessionLocal() as db:
        try:
            db.delete(todo)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print("Error al borrar la To Do:", e)
            return False
        
def get_todo_by_id(todo_id: int):
    with SessionLocal() as db:
        try:
            return db.query(ToDo).filter(ToDo.id == todo_id).options(joinedload(ToDo.creator)).first()
        except Exception as e:
            print("Error al buscar la To Do:", e)

    
def get_all_todos():
    with SessionLocal() as db:
        todos = db.query(ToDo).options(joinedload(ToDo.creator)).all() 
        return todos
