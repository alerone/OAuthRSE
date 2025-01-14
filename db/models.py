from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship  
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    picture = Column(String, nullable=True)

     # Relación con los ToDos
    todos = relationship("ToDo", back_populates="creator")


class ToDo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Clave foránea para relacionar con el usuario
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    photo_id = Column(String, nullable=True)

    # Relación con User
    creator = relationship("User", back_populates="todos")
