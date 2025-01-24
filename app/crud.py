from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from datetime import date, timedelta, datetime, time
import logging
from fastapi import Request
from sqlalchemy import or_



#=============================== S O C I O S ================================================
def create_socio(db: Session, socio: schemas.SocioCreate):
    # Crear un nuevo socio en la base de datos a partir del objeto `SocioCreate`
    db_socio = models.Socio(**socio.dict())  # Usa el modelo de la base de datos
    db.add(db_socio)
    db.commit()
    db.refresh(db_socio)  # Recuperar el objeto con el ID autogenerado
    return db_socio

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_socios(db: Session):
    return db.query(models.Socio).options(joinedload(models.Socio.pagos)).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_socio(db: Session, socio_id: int):
    return db.query(models.Socio).options(joinedload(models.Socio.pagos)).filter(models.Socio.id_socio == socio_id).first()


#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def update_socio(db: Session, socio_id: int, socio_update: schemas.SocioUpdate):
    socio = get_socio(db, socio_id)
    if not socio:
        raise ValueError(f"No se encontró el socio con ID {socio_id}")
    for key, value in socio_update.dict(exclude_unset=True).items():
        setattr(socio, key, value)
    db.commit()
    db.refresh(socio)  # Asegura que los cambios se reflejen en el objeto
    return socio

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def delete_socio(db: Session, socio_id: int) -> dict:
    try:
        # Eliminar los pagos asociados
        db.query(models.Pago).filter(models.Pago.id_socio == socio_id).delete()
        db.commit()

        # Ahora eliminar el socio
        socio = db.query(models.Socio).filter(models.Socio.id_socio == socio_id).first()
        if not socio:
            return {"status": "error", "message": "Socio no encontrado"}
        
        db.delete(socio)
        db.commit()

        return {"status": "success"}
    except Exception as e:
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
# Actualización de la función `obtener_pagos_pendientes` para trabajar con el tipo `Date`
def obtener_pagos_pendientes(db: Session, fecha_inicio: date, fecha_fin: date):
    """
    Obtiene los pagos pendientes para el rango de fechas especificado.
    """
    try:
        # Mostrar las fechas para depuración
        print(f"Fecha inicio en la consulta: {fecha_inicio}")
        print(f"Fecha fin en la consulta: {fecha_fin}")

        # Aplicar filtros de rango de fechas en la consulta
        pagos = (
            db.query(
                models.Socio.nombre,
                models.Socio.apellido,
                models.Plan.nombre_plan.label("combo"),
                models.Plan.precio,
                models.Pago.fecha_programada,
                models.Pago.fecha_pago,
                models.Pago.estado_pago,
                models.Pago.id_pago
            )
            .join(models.Plan, models.Socio.id_plan == models.Plan.id_plan)
            .join(models.Pago, models.Socio.id_socio == models.Pago.id_socio)
            .filter(models.Pago.fecha_programada >= fecha_inicio)  # Filtro de fecha de inicio
            .filter(models.Pago.fecha_programada <= fecha_fin)    # Filtro de fecha de fin
            .all()
        )

        if not pagos:
            print(f"No se encontraron pagos pendientes para el rango de fechas {fecha_inicio} a {fecha_fin}.")
        
        return pagos

    except Exception as e:
        print(f"Error al obtener pagos pendientes: {e}")
        return []


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


#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

#=============================== P A G O S ================================================
def create_pago(db: Session, id_socio: int, id_plan: int, fecha_pago: str):
    # Crear un nuevo pago para el socio
    db_pago = schemas.Pago(
        id_socio=id_socio,
        id_plan=id_plan,
        fecha_programada=fecha_pago,  # Este será el primer día del mes
        fecha_pago=None,  # Este campo estará vacío hasta que el pago se realice
        estado_pago='Pendiente',  # El estado inicial del pago es 'Pendiente'
        mes_correspondiente=fecha_pago  # El mes correspondiente al pago
    )
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    return db_pago

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
# CRUD para obtener un pago
def get_pago(db: Session, id_pago: int):
    return db.query(models.Pago).filter(models.Pago.id_pago == id_pago).first()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def actualizar_cobro(db: Session, id_pago: int, fecha_pago: str):
    pago = get_pago(db, id_pago)
    if not pago:
        return None
    pago.fecha_pago = fecha_pago
    pago.estado_pago = "Pagado"
    db.commit()
    return pago


#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

def get_all_pagos(db: Session):
    return db.query(models.Pago).all()

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
