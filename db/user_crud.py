from .models import User
from .database import SessionLocal

def create_user(name, email, picture):
    db = SessionLocal()
    try:
        new_user = User(name=name, email=email, picture=picture)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except Exception as e:
        db.rollback()
        print("Error al crear usuario:", e)
    
    finally:
        db.close()

def get_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()

def get_user_by_email(email):
    with SessionLocal() as db:
        # Consulta si existe un usuario con el email especificado
        return db.query(User).filter(User.email == email).first()

def exist_user(email):
    """Verifica si un usuario existe en la base de datos por su email."""
    with SessionLocal() as db:
        # Consulta si existe un usuario con el email especificado
        return db.query(User).filter(User.email == email).first() is not None

