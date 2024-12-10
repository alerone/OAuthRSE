from .models import ToDo
from .database import SessionLocal 
from sqlalchemy.orm import joinedload

def create_todo(name: str, description: str, created_by: int):
    db = SessionLocal()
    try:
        new_todo = ToDo(name=name, description=description, created_by=created_by)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    
    except Exception as e:
        db.rollback()
        print("Error al crear la To Do:", e)
    
    finally:
        db.close()
    
def get_all_todos():
    with SessionLocal() as db:
        todos = db.query(ToDo).options(joinedload(ToDo.creator)).all() 
        return todos