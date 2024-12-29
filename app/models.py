from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Text, Boolean, Time
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base

#=============================== C O M B O S ================================================
class Plan(Base):
    __tablename__ = 'planes'
    id_plan = Column(Integer, primary_key=True, autoincrement=True)
    nombre_plan = Column(String(100), nullable=False)
    dias = Column(Integer, nullable=False) 
    descripcion = Column(Text, nullable=True)  
    precio = Column(Integer,nullable=False)

    # Relaciones
    socios = relationship("Socio", back_populates="plan")

#=============================== PLANES S O C I A L E S ================================================
class PlanSocial(Base):
    __tablename__ = 'planes_sociales'
    id_plan_social = Column(Integer, primary_key=True, autoincrement=True)
    nombre_plan_social = Column(String(100), nullable=False)

    # Relaciones
    socios = relationship("Socio", back_populates="plan_social")

#=============================== S O C I O S ================================================
class Socio(Base):
    __tablename__ = 'socios'
    id_socio = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    dni = Column(Integer, unique=True, nullable=False)
    fecha_nacimiento = Column(Date)
    genero = Column(String(50))
    email = Column(String(150))
    telefono = Column(String(20))
    direccion = Column(String(255))
    id_plan = Column(Integer, ForeignKey('planes.id_plan'))
    id_plan_social = Column(Integer, ForeignKey('planes_sociales.id_plan_social'))

    # Relaciones
    plan = relationship("Plan", back_populates="socios")
    plan_social = relationship("PlanSocial", back_populates="socios")
    asistencias = relationship("Asistencia", back_populates="socio")

#=============================== A S I S T E N C I A S ================================================
class Asistencia(Base):
    __tablename__ = 'asistencias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    socio_id = Column(Integer, ForeignKey('socios.id_socio'), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    # Relaciones
    socio = relationship("Socio", back_populates="asistencias")

#=============================== L O G I N ================================================
class login(Base):
    __tablename__ = 'login'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(50),unique=True, nullable=False)
    password=Column(String(50),nullable=True)