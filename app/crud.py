from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date, timedelta
import logging
from fastapi import Request
from datetime import time
from sqlalchemy import or_ , text , func



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

def delete_socio(db: Session, socio_id: int) -> dict:
    try:
        socio = db.query(models.Socio).filter(models.Socio.id_socio == socio_id).first()
        if not socio:
            print(f"Socio con ID {socio_id} no encontrado.")
            return {"status": "error", "message": "Socio no encontrado"}
        
        print(f"Socio encontrado: {socio}")
        db.delete(socio)
        db.commit()
        print(f"Socio con ID {socio_id} eliminado exitosamente.")
        return {"status": "success"}
    except Exception as e:
        print(f"Error al eliminar el socio: {str(e)}")
        db.rollback()
        return {"status": "error", "message": f"Error al eliminar: {str(e)}"}


#=============================== PLANES S O C I A L E S ================================================

def get_plan_social(db: Session, plan_social_id: int):
    return db.query(models.PlanSocial).filter(models.PlanSocial.id_plan_social == plan_social_id).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_all_planes_sociales(db: Session):
    return db.query(models.PlanSocial).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def create_plan_social(db: Session, plan_social: schemas.PlanSocialCreate):
    nuevo_plan = models.PlanSocial(**plan_social.dict())
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_plan_social(db: Session, plan_social_id: int, plan_social_update: schemas.PlanSocialUpdate):
    plan_db = get_plan_social(db, plan_social_id)
    if plan_db:
        for key, value in plan_social_update.dict(exclude_unset=True).items():
            setattr(plan_db, key, value)
        db.commit()
        db.refresh(plan_db)
    return plan_db

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

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

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_all_planes(db: Session):
    return db.query(models.Plan).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def create_plan(db: Session, plan: schemas.PlanCreate):
    nuevo_plan = models.Plan(**plan.dict())
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_plan(db: Session, plan_id: int, plan_update: schemas.PlanUpdate):
    plan_db = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if plan_db:
        for key, value in plan_update.dict(exclude_unset=True).items():
            setattr(plan_db, key, value)
        db.commit()
        db.refresh(plan_db)
    return plan_db

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_plan(db: Session, plan_id: int):
    plan = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if not plan:
        return {"status": "error", "message": "Plan no encontrado"}
    
    db.delete(plan)
    db.commit()
    return {"status": "success", "message": "Plan eliminado correctamente"}

#=============================== A S I S T E N C I A S ================================================

def create_asistencia(db: Session, asistencia: schemas.AsistenciaCreate):
    db_asistencia = models.Asistencia(
        socio_id=asistencia.socio_id,
        fecha=asistencia.fecha,
        hora=asistencia.hora
    )
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_all_asistencias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asistencia).offset(skip).limit(limit).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def eliminar_asistencia(db: Session, asistencia_id: int):
    asistencia = db.query(models.Asistencia).filter(models.Asistencia.id == asistencia_id).first()
    if not asistencia:
        return False
    db.delete(asistencia)
    db.commit()
    return True

#=============================== L O G I N ================================================
# Crear usuario
def create_login(db: Session, login_data: schemas.LoginCreate):
    db_login = models.Login(**login_data.dict())  # Crear una instancia del modelo
    db.add(db_login)  # Agregar a la sesión
    db.commit()  # Guardar cambios
    db.refresh(db_login)  # Actualizar el objeto con la información de la base de datos
    return db_login

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener usuario por nombre
def get_login_by_name(db: Session, name: str):
    return db.query(models.login).filter(models.login.name == name).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def log_logout(db: Session, user_id: int):
    logging.info(f"Usuario con ID {user_id} ha cerrado sesión.")
    return True

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def check_authenticated(request: Request) -> bool:
    """
    Verifica si el usuario está autenticado mediante la cookie 'authenticated'.
    """
    return request.cookies.get("authenticated") == "true"



#=============================== P R U E B A ================================================
def get_all_socios(db: Session):
    return db.query(models.Socio).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_asistencias_by_date(db: Session, fecha: str):
    return db.query(models.Asistencia).filter(models.Asistencia.fecha == fecha).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_asistencias_by_socio(db: Session, socio: str):
    return (
        db.query(models.Asistencia)
        .join(models.Socio)
        .filter(or_(
            models.Socio.nombre.ilike(f"%{socio}%"),
            models.Socio.apellido.ilike(f"%{socio}%")
        ))
        .all()
    )

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_asistencia(db: Session, asistencia_id: int, socio_id: int):
    asistencia = db.query(models.Asistencia).filter(models.Asistencia.id == asistencia_id).first()
    if not asistencia:
        return {"status": "error", "message": "Asistencia no encontrada"}
    asistencia.socio_id = socio_id
    db.commit()
    return {"status": "success", "message": "Asistencia actualizada"}

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_asistencias_by_socio(db: Session, socio: str):
    try:
        result = db.query(models.Asistencia).join(models.Socio).filter(models.Socio.nombre.like(f'%{socio}%')).all()
        return result
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def convert_to_string(hour: time):
    return hour.strftime("%H:%M:%S") if hour else None    
    


#=============================== C O B R O S ================================================

def get_socios_cobro_semanal(db: Session, start_of_week: date, end_of_week: date):
    """
    Obtiene los socios cuya fecha de cobro (fecha_ingreso + 30 días) cae en el rango de la semana actual.
    """
    socios = (
        db.query(models.Socio)
        .filter(
            models.Socio.fecha_ingreso.isnot(None),
            func.date_add(models.Socio.fecha_ingreso, text("INTERVAL 30 DAY")) >= start_of_week,
            func.date_add(models.Socio.fecha_ingreso, text("INTERVAL 30 DAY")) <= end_of_week,
        )
        .all()
    )

    # Log para depuración
    print(f"Socios encontrados para el rango {start_of_week} - {end_of_week} ({len(socios)} registros):")
    for socio in socios:
        fecha_cobro = socio.fecha_ingreso + timedelta(days=30)
        print(f"Nombre: {socio.nombre}, Apellido: {socio.apellido}, Fecha Cobro: {fecha_cobro}")

    return socios



#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
def calcular_fechas_cobro(fecha_ingreso, fecha_actual):
    """
    Calcula todas las fechas de cobro mensuales para un socio
    desde su fecha de ingreso hasta la fecha actual.
    """
    fechas_cobro = []
    fecha_cobro = fecha_ingreso + timedelta(days=30)
    
    while fecha_cobro <= fecha_actual:
        fechas_cobro.append(fecha_cobro)
        fecha_cobro += timedelta(days=30)  # Incremento mensual
    
    return fechas_cobro

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
def filtrar_fechas_semana_actual(fechas_cobro, start_of_week, end_of_week):
    """
    Filtra las fechas de cobro que caen dentro de la semana actual.
    """
    return [fecha for fecha in fechas_cobro if start_of_week <= fecha <= end_of_week]

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
def get_socios_cobro_semana_anterior(db: Session):
    """
    Obtiene los socios cuya fecha de cobro (fecha_ingreso + múltiplos de 30 días) cayó en la semana anterior.
    """
    today = date.today()
    start_of_last_week = today - timedelta(days=today.weekday() + 7)  # Lunes de la semana pasada
    end_of_last_week = start_of_last_week + timedelta(days=6)  # Domingo de la semana pasada

    # Consulta ajustada para incluir fechas acumulativas de cobro
    socios = (
        db.query(models.Socio)
        .filter(
            models.Socio.fecha_ingreso.isnot(None),
            func.date_add(
                models.Socio.fecha_ingreso, 
                text("INTERVAL 30 * FLOOR(DATEDIFF(:start_date, fecha_ingreso) / 30) DAY")
            ) >= start_of_last_week,
            func.date_add(
                models.Socio.fecha_ingreso, 
                text("INTERVAL 30 * FLOOR(DATEDIFF(:start_date, fecha_ingreso) / 30) DAY")
            ) <= end_of_last_week,
        )
        .params(start_date=end_of_last_week)  # Pasamos el parámetro para la consulta SQL
        .all()
    )

    # Log para depuración
    print(f"Socios encontrados para la semana anterior ({len(socios)} registros):")
    for socio in socios:
        # Calculamos la fecha de cobro acumulativa
        dias_transcurridos = (start_of_last_week - socio.fecha_ingreso).days
        ciclos_completos = dias_transcurridos // 30
        fecha_cobro = socio.fecha_ingreso + timedelta(days=30 * ciclos_completos)
        print(f"Nombre: {socio.nombre}, Apellido: {socio.apellido}, Fecha Cobro: {fecha_cobro}")

    return socios