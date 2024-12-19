from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date, timedelta
from typing import Dict


#=============================== S O C I O S ================================================
def create_socio(db: Session, socio: schemas.SocioCreate):
    db_socio = models.Socio(**socio.dict())
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)
    return db_socio

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_socios(db: Session):
    return db.query(models.Socio).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_socio(db: Session, socio_id: int):
    return db.query(models.Socio).filter(models.Socio.id_socio == socio_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_socio(db: Session, socio_id: int, socio_update: schemas.SocioUpdate):
    socio = get_socio(db, socio_id)
    if not socio:
        return None
    for key, value in socio_update.dict(exclude_unset=True).items():
        setattr(socio, key, value)
    db.commit()
    return socio

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_socio(db: Session, socio_id: int):
    socio = get_socio(db, socio_id)
    if socio:
        db.delete(socio)
        db.commit()
        return {"status": "success"}
    return {"status": "error", "message": "Socio no encontrado"}


#=============================== PLANES S O C I A L E S ================================================

def get_plan_social(db: Session, plan_social_id: int):
    return db.query(models.PlanSocial).filter(models.PlanSocial.id_plan_social == plan_social_id).first()

def get_all_planes_sociales(db: Session):
    return db.query(models.PlanSocial).all()

def create_plan_social(db: Session, plan_social: schemas.PlanSocialCreate):
    nuevo_plan = models.PlanSocial(**plan_social.dict())
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan

def update_plan_social(db: Session, plan_social_id: int, plan_social_update: schemas.PlanSocialUpdate):
    plan_db = get_plan_social(db, plan_social_id)
    if plan_db:
        for key, value in plan_social_update.dict(exclude_unset=True).items():
            setattr(plan_db, key, value)
        db.commit()
        db.refresh(plan_db)
    return plan_db

def delete_plan_social(db: Session, plan_social_id: int):
    plan_db = db.query(models.PlanSocial).filter(models.PlanSocial.id_plan_social == plan_social_id).first()
    
    if plan_db:
        db.delete(plan_db)
        db.commit()
        return {"status": "success"}
    
    return {"status": "failure", "message": "Plan social no encontrado"}

#=============================== C O M B O S ================================================
def get_plan(db: Session, plan_id: int):
    return db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()

def get_all_planes(db: Session):
    return db.query(models.Plan).all()

def create_plan(db: Session, plan: schemas.PlanCreate):
    nuevo_plan = models.Plan(**plan.dict())
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan

def update_plan(db: Session, plan_id: int, plan_update: schemas.PlanUpdate):
    plan_db = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if plan_db:
        for key, value in plan_update.dict(exclude_unset=True).items():
            setattr(plan_db, key, value)
        db.commit()
        db.refresh(plan_db)
    return plan_db

def delete_plan(db: Session, plan_id: int):
    plan = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if not plan:
        return {"status": "error", "message": "Plan no encontrado"}
    
    db.delete(plan)
    db.commit()
    return {"status": "success", "message": "Plan eliminado correctamente"}

#=============================== A S I S T E N C I A S ================================================

def registrar_asistencia(db: Session, asistencias: Dict[int, bool]):
    """
    Registra las asistencias en la base de datos.
    :param asistencias: Diccionario {socio_id: asistencia (True/False)}
    """
    for socio_id, asistio in asistencias.items():
        fecha_actual = date.today()
        # Verificar si ya existe asistencia para este socio en la fecha actual
        asistencia_existente = db.query(models.Asistencia).filter(
            models.Asistencia.socio_id == socio_id,
            models.Asistencia.fecha == fecha_actual
        ).first()

        if asistio and not asistencia_existente:
            # Crear nueva asistencia
            nueva_asistencia = models.Asistencia(socio_id=socio_id, fecha=fecha_actual)
            db.add(nueva_asistencia)
        elif not asistio and asistencia_existente:
            # Eliminar asistencia si se desmarcó
            db.delete(asistencia_existente)

    db.commit()
    return {"message": "Asistencias registradas correctamente."}

def obtener_asistencias_por_mes(db: Session, year: int, month: int):
    socios = db.query(models.Socio).all()
    resultado = []

    # Obtener el primer día y el último día del mes
    primer_dia = date(year, month, 1)
    if month == 12:
        ultimo_dia = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia = date(year, month + 1, 1) - timedelta(days=1)

    for socio in socios:
        asistencias = db.query(models.Asistencia).filter(
            models.Asistencia.socio_id == socio.id_socio,
            models.Asistencia.fecha >= primer_dia,
            models.Asistencia.fecha <= ultimo_dia
        ).all()
        resultado.append({
            "socio": socio.nombre,
            "asistencias": [asistencia.fecha.day for asistencia in asistencias],
        })

    return resultado


def guardar_asistencias(db: Session, asistencias: list[dict], year: int, month: int):
    for asistencia in asistencias:
        socio = db.query(models.Socio).filter(models.Socio.nombre == asistencia["socio"]).first()
        if not socio:
            continue

        fecha = date(year, month, int(asistencia["dia"]))
        # Cambiar `socio.id` a `socio.id_socio`
        if not db.query(models.Asistencia).filter(
            models.Asistencia.socio_id == socio.id_socio,
            models.Asistencia.fecha == fecha
        ).first():
            nueva_asistencia = models.Asistencia(socio_id=socio.id_socio, fecha=fecha)
            db.add(nueva_asistencia)

    db.commit()
    return {"message": "Asistencias guardadas correctamente"}

#=============================== L O G I N ================================================
# Crear usuario
def create_login(db: Session, login_data: schemas.LoginCreate):
    db_login = models.Login(**login_data.dict())  # Crear una instancia del modelo
    db.add(db_login)  # Agregar a la sesión
    db.commit()  # Guardar cambios
    db.refresh(db_login)  # Actualizar el objeto con la información de la base de datos
    return db_login

# Obtener usuario por nombre
def get_login_by_name(db: Session, name: str):
    return db.query(models.login).filter(models.login.name == name).first()
