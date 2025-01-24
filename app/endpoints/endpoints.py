from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from fastapi.templating import Jinja2Templates
import logging
from sqlalchemy.exc import  SQLAlchemyError
from fastapi import Query
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError



logging.basicConfig(level=logging.DEBUG)

# Crear un router principal
router = APIRouter()

# Crear un objeto Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#=============================== S O C I O S ================================================
# Mostrar formulario para crear socio
@router.get("/crear_socio", response_class=HTMLResponse, tags=["Socios"])
async def show_create_socio_form(request: Request, db: Session = Depends(get_db),message: str = None):
    # Obtener planes y planes sociales
    planes = crud.get_all_planes(db)
    planes_sociales = crud.get_all_planes_sociales(db)

    # Pasar estos datos al template
    return templates.TemplateResponse("crear_socio.html", {
        "request": request,
        "planes": planes,
        "planes_sociales": planes_sociales,
        "message": message  # Aquí pasamos el mensaje de estado
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
from app import models

# Crear un socio (POST)
# Crear un socio (POST)
@router.post("/crear_socio", response_class=HTMLResponse, tags=["Socios"])
async def create_socio(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    dni: int = Form(...),
    fecha_nacimiento: str = Form(...),
    genero: str = Form(...),
    email: str = Form(None),
    telefono: str = Form(None),
    direccion: str = Form(None),
    fecha_programada: str = Form(...),  # Esto es para la fecha de pago
    id_plan: int = Form(...),  # Asegúrate de que id_plan no sea None
    id_plan_social: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Verificar que el plan existe
        plan = db.query(models.Plan).filter(models.Plan.id_plan == id_plan).first()
        if not plan:
            raise ValueError("El plan con ID {} no existe.".format(id_plan))

        # Verificar si el plan social existe (si se proporciona)
        plan_social = None
        if id_plan_social:
            plan_social = db.query(models.PlanSocial).filter(models.PlanSocial.id_plan_social == id_plan_social).first()
            if not plan_social:
                raise ValueError("El plan social con ID {} no existe.".format(id_plan_social))

        # Crear el socio
        socio_data = schemas.SocioCreate(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            email=email,
            telefono=telefono,
            direccion=direccion,
            id_plan=id_plan,  # Asegurarse de que el plan no sea None
            id_plan_social=id_plan_social,
        )
        db_socio = crud.create_socio(db, socio_data)

        # Crear los pagos para el socio, separados por mes
        fecha_programada_date = datetime.strptime(fecha_programada, '%Y-%m-%d')
        for mes in range(1, 13):  # Crear pagos para 12 meses
            fecha_pago = datetime(fecha_programada_date.year, mes, 1)  # Primer día de cada mes
            crud.create_pago(db, db_socio.id_socio, id_plan, fecha_pago.strftime('%Y-%m-%d'))

        message = "Socio creado exitosamente."
    except IntegrityError as e:
        message = f"Error al crear el socio: {str(e)}"
    except ValueError as ve:
        message = str(ve)
    except Exception as e:
        message = f"Error al crear el socio: {str(e)}"
    
    # Redirigir a la misma página después de crear el socio
    url = str(request.url_for("show_create_socio_form"))
    return RedirectResponse(url=f"{url}?message={message}", status_code=303)








#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Leer todos los socios
@router.get("/read_socios", response_class=HTMLResponse, tags=["Socios"])
async def read_socios(request: Request, db: Session = Depends(get_db), message: str = None):
    socios = crud.get_socios(db)
    return templates.TemplateResponse("read_socios.html", {
        "request": request, 
        "socios": socios,
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener un socio por ID (GET)
@router.get("/socios/{socio_id}", response_model=schemas.Socio, tags=["Socios"])
async def read_socio(socio_id: int, db: Session = Depends(get_db)):
    socio = crud.get_socio(db, socio_id)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Ruta GET para mostrar el formulario de selección de socio
@router.get("/actualizar_socio/{socio_id}", response_class=HTMLResponse, tags=["Socios"])
async def mostrar_formulario_actualizacion(request: Request, socio_id: int, db: Session = Depends(get_db)):
    """
    Muestra el formulario para actualizar los datos del socio dado su ID.
    """
    socio = crud.get_socio(db, socio_id)
    if not socio:
        return templates.TemplateResponse("read_socios.html", {
            "request": request,
            "socios": crud.get_all_socios(db),
            "message": f"Socio con ID {socio_id} no encontrado.",
        })

    planes = crud.get_all_planes(db)
    planes_sociales = crud.get_all_planes_sociales(db)

    return templates.TemplateResponse("actualizar_socio.html", {
        "request": request,
        "socio": socio,
        "planes": planes,
        "planes_sociales": planes_sociales,
        "message": None,
    })

@router.post("/actualizar_socio", response_class=HTMLResponse, tags=["Socios"])
async def mostrar_formulario_actualizacion(
    request: Request,
    socio_id: int = Form(...),  # Recibe el ID del socio
    db: Session = Depends(get_db),
):
    """
    Muestra el formulario para actualizar los datos del socio.
    """
    socio = crud.get_socio(db, socio_id)
    if not socio:
        return templates.TemplateResponse("ver_socios.html", {
            "request": request,
            "socios": crud.get_all_socios(db),
            "message": "Socio no encontrado",
        })

    planes = crud.get_all_planes(db)
    planes_sociales = crud.get_all_planes_sociales(db)

    return templates.TemplateResponse("actualizar_socio.html", {
        "request": request,
        "socio": socio,
        "planes": planes,
        "planes_sociales": planes_sociales,
        "message": None,
    })


@router.post("/guardar_actualizacion", response_class=HTMLResponse, tags=["Socios"])
async def guardar_actualizacion(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    dni: int = Form(...),
    fecha_nacimiento: str = Form(...),
    genero: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    fecha_ingreso: str = Form(...),
    id_plan: int = Form(...),
    id_plan_social: int = Form(...),
    socio_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """
    Guarda los cambios realizados en los datos del socio.
    """
    socio = crud.get_socio(db, socio_id)
    if not socio:
        return templates.TemplateResponse("ver_socios.html", {
            "request": request,
            "socios": crud.get_all_socios(db),
            "message": "Socio no encontrado",
        })

    # Convertir fecha_ingreso a datetime antes de actualizar
    try:
        socio.fecha_ingreso = datetime.strptime(fecha_ingreso, "%Y-%m-%d")
    except ValueError:
        return templates.TemplateResponse("ver_socios.html", {
            "request": request,
            "socios": crud.get_all_socios(db),
            "message": "Formato de fecha incorrecto",
        })

    # Actualizar los campos del socio
    socio.nombre = nombre
    socio.apellido = apellido
    socio.dni = dni
    socio.fecha_nacimiento = fecha_nacimiento
    socio.genero = genero
    socio.email = email
    socio.telefono = telefono
    socio.direccion = direccion
    socio.id_plan = id_plan
    socio.id_plan_social = id_plan_social

    db.commit()  # Guardar cambios en la base de datos
    db.refresh(socio)  # Refrescar los datos del socio

    return templates.TemplateResponse("read_socios.html", {
        "request": request,
        "socios": crud.get_all_socios(db),
        "message": "Socio actualizado exitosamente",
    })


#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar un socio (POST)
@router.post("/socios/{socio_id}/eliminar", response_class=JSONResponse, tags=["Socios"])
async def delete_socio(request: Request, socio_id: int, db: Session = Depends(get_db)):
    try:
        # Llamada al método de CRUD para eliminar el socio
        result = crud.delete_socio(db, socio_id)
        if result.get("status") == "success":
            return {"success": True, "message": "Socio eliminado exitosamente"}
        else:
            return {"success": False, "message": result.get("message", "Error al eliminar el socio")}
    except SQLAlchemyError as e:
        db.rollback()
        return {"success": False, "message": f"Error de base de datos: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"Error inesperado: {str(e)}"}
#=============================== PLANES S O C I A L E S ================================================

# Mostrar formulario para crear un plan social
@router.get("/crear_plan_social", response_class=HTMLResponse, tags=["Planes sociales"])
async def show_create_plan_social_form(request: Request):
    return templates.TemplateResponse("crear_plan_social.html", {"request": request})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Crear un nuevo plan social
@router.post("/crear_plan_social", response_class=HTMLResponse, tags=["Planes sociales"])
async def create_plan_social(
    request: Request,
    nombre_plan_social: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        plan_data = schemas.PlanSocialCreate(nombre_plan_social=nombre_plan_social)
        crud.create_plan_social(db, plan_data)
        message = f"Plan social '{nombre_plan_social}' creado exitosamente."
    except Exception as e:
        message = f"Error al crear el plan social: {str(e)}"
    
    return templates.TemplateResponse("crear_plan_social.html", {
        "request": request,
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Leer todos los planes sociales
@router.get("/read_planes_sociales", response_class=HTMLResponse, tags=["Planes sociales"])
async def read_planes_sociales(request: Request, db: Session = Depends(get_db)):
    planes_sociales = crud.get_all_planes_sociales(db)  # Cambiado a get_all_planes_sociales
    return templates.TemplateResponse("read_planes_sociales.html", {
        "request": request,
        "planes_sociales": planes_sociales
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener un plan social por ID
@router.get("/planes_sociales/{plan_social_id}", response_class=HTMLResponse, tags=["Planes sociales"])
async def read_plan_social(plan_social_id: int, db: Session = Depends(get_db)):
    plan_social = crud.get_plan_social(db, plan_social_id)
    if plan_social is None:
        raise HTTPException(status_code=404, detail="Plan social no encontrado")
    return templates.TemplateResponse("detalle_plan_social.html", {
        "plan_social": plan_social
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar un plan social
@router.post("/planes_sociales/{plan_social_id}/actualizar", response_class=HTMLResponse, tags=["Planes sociales"])
async def update_plan_social(
    plan_social_id: int,
    request: Request,
    nombre_plan_social: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        plan_social_update = schemas.PlanSocialUpdate(nombre_plan_social=nombre_plan_social)
        plan_actualizado = crud.update_plan_social(db, plan_social_id, plan_social_update)
        if not plan_actualizado:
            raise HTTPException(status_code=404, detail="Plan social no encontrado")
        message = "Plan social actualizado exitosamente."
    except Exception as e:
        message = f"Error al actualizar el plan social: {str(e)}"

    return templates.TemplateResponse("detalle_plan_social.html", {
        "request": request,
        "message": message,
        "plan_social": plan_actualizado
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar un plan social
@router.post("/planes_sociales/{plan_social_id}/eliminar", tags=["Planes sociales"])
async def delete_plan_social(plan_social_id: int, db: Session = Depends(get_db)):
    result = crud.delete_plan_social(db, plan_social_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return {"message": "Plan social eliminado exitosamente"}

#=============================== C O M B O S ================================================
# Mostrar formulario para crear un combo (get)
@router.get("/crear_plan", response_class=HTMLResponse, tags=["Combos"])
async def show_create_plan_form(request: Request):
    return templates.TemplateResponse("crear_plan.html", {"request": request})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
# Mostrar formulario para crear un combo (post)
@router.post("/crear_plan", response_class=HTMLResponse, tags=["Combos"])
async def create_plan_endpoint(
    request: Request,
    nombre_plan: str = Form(...),
    dias: int = Form(...),
    descripcion: str = Form(None),
    precio : int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        plan_data = schemas.PlanCreate(nombre_plan=nombre_plan, dias=dias, descripcion=descripcion, precio=precio)
        crud.create_plan(db, plan_data)
        message = f"Plan '{nombre_plan}' creado exitosamente."
    except Exception as e:
        message = f"Error al crear el plan: {str(e)}"
    
    return templates.TemplateResponse("crear_plan.html", {
        "request": request,
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Leer todos los combos
@router.get("/read_combos", response_class=HTMLResponse, tags=["Combos"])
async def read_planes(request: Request, db: Session = Depends(get_db)):
    planes = crud.get_all_planes(db)
    return templates.TemplateResponse("read_combos.html", {
        "request": request,
        "combos": planes
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Obtener un combo por ID (detalles)
@router.get("/planes/{plan_id}", response_class=HTMLResponse, tags=["Combos"])
async def read_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    plan = crud.get_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return templates.TemplateResponse("detalle_plan.html", {
        "request": request,
        "plan": plan
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Actualizar un combo
@router.post("/planes/{plan_id}/actualizar", response_class=HTMLResponse, tags=["Combos"])
async def update_plan_endpoint(
    plan_id: int,
    request: Request,
    nombre_plan: str = Form(...),
    dias: int = Form(...),
    descripcion: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        plan_update = schemas.PlanUpdate(nombre_plan=nombre_plan, dias=dias, descripcion=descripcion)
        plan_actualizado = crud.update_plan(db, plan_id, plan_update)
        if not plan_actualizado:
            raise HTTPException(status_code=404, detail="Plan no encontrado")
        message = "Plan actualizado exitosamente."
    except Exception as e:
        message = f"Error al actualizar el plan: {str(e)}"

    return templates.TemplateResponse("detalle_plan.html", {
        "request": request,
        "message": message,
        "plan": plan_actualizado
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar un combo
@router.post("/planes/{plan_id}/eliminar", status_code=200, tags=["Combos"])
async def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    result = crud.delete_plan(db, plan_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": result["message"]}



#=============================== A S I S T E N C I A S ================================================
# Mostrar formulario para registrar asistencia
@router.get("/crear_asistencia", response_class=HTMLResponse, tags=["Asistencias"])
async def show_create_asistencia_form(request: Request, db: Session = Depends(get_db)):
    socios = crud.get_all_socios(db)
    return templates.TemplateResponse("crear_asistencia.html", {"request": request, "socios": socios})

@router.post("/crear_asistencia", tags=["Asistencias"])
async def create_asistencia(
    asistencia: schemas.AsistenciaBase,  # Pydantic model
    db: Session = Depends(get_db)
):
    try:
        # Verifica lo que recibe el backend
        print(f"Hora recibida en backend: {asistencia.hora}")

        # Convierte la hora si es un string
        if isinstance(asistencia.hora, str):
            asistencia.hora = datetime.strptime(asistencia.hora, "%H:%M:%S").time()

        # Asegúrate de que la hora esté en formato time
        print(f"Hora convertida: {asistencia.hora}")

        # Crear la asistencia (puedes seguir con la lógica de base de datos aquí)
        crud.create_asistencia(db, asistencia)
        return {"message": "Asistencia registrada exitosamente."}
    except Exception as e:
        print(f"Error al registrar la asistencia: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al registrar asistencia: {str(e)}")


#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Leer todas las asistencias
@router.get("/read_asistencias", response_class=HTMLResponse, tags=["Asistencias"])
async def read_asistencias(request: Request, db: Session = Depends(get_db)):
    asistencias = crud.get_all_asistencias(db)
    return templates.TemplateResponse("read_asistencias.html", {
        "request": request,
        "asistencias": asistencias
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/asistencias", response_model=List[schemas.Asistencia], tags=["Asistencias"])
async def get_all_asistencias(db: Session = Depends(get_db)):
    return crud.get_all_asistencias(db)

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar una asistencia
@router.post("/read_asistencias/{asistencia_id}/eliminar", tags=["Asistencias"])
async def delete_asistencia(asistencia_id: int, db: Session = Depends(get_db)):
    result = crud.delete_asistencia(db, asistencia_id)

    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])

    return {"message": "Asistencia eliminada exitosamente"}

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/read_asistencias/filtrar", response_class=HTMLResponse, tags=["Asistencias"])
async def filter_asistencias(
    request: Request,
    fecha: str = Query(None),
    db: Session = Depends(get_db)
):
    asistencias = crud.get_asistencias_by_date(db, fecha) if fecha else []
    return templates.TemplateResponse("read_asistencias.html", {
        "request": request,
        "asistencias": asistencias
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/read_asistencias/informe", response_class=HTMLResponse, tags=["Asistencias"])
async def informe_asistencias(
    request: Request,
    socio: str = Query(None),
    db: Session = Depends(get_db)
):
    # Recuperamos las asistencias filtradas por socio si el parámetro 'socio' está presente
    asistencias = crud.get_asistencias_by_socio(db, socio) if socio else []
    
    # Retornamos el archivo de plantilla correcto 'read_asistencias.html'
    return templates.TemplateResponse("read_asistencias.html", {
        "request": request,
        "asistencias": asistencias,
        "socio": socio
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/read_asistencias/{asistencia_id}/actualizar", response_class=HTMLResponse, tags=["Asistencias"])
async def update_asistencia(
    request: Request,
    asistencia_id: int,
    socio_id: int = Form(...),
    db: Session = Depends(get_db)
):
    result = crud.update_asistencia(db, asistencia_id, socio_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": "Asistencia actualizada exitosamente"}

#=============================== L O G I N ================================================

@router.get("/login" , tags=["Login"])
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Endpoint de autenticación
@router.post("/login" , tags=["Login"])
def login(request: Request, name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.get_login_by_name(db, name)
    if user and user.password == password:
        response = RedirectResponse(url="/index", status_code=303)
        response.set_cookie(key="authenticated", value="true")
        return response
    else:
        response = RedirectResponse(url="/login", status_code=303)
        response.set_cookie(key="login_error", value="Credenciales incorrectas", max_age=10)
        return response
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
    
@router.get("/index" , tags=["Login"])
def show_index(request: Request):
    authenticated = request.cookies.get("authenticated")
    if authenticated == "true":
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return RedirectResponse(url="/login")
    
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.get("/logout", tags=["Login"])
def logout(response: Response):
    response.delete_cookie("authenticated")
    return RedirectResponse(url="/login")


#=============================== C O B R O S ================================================

@router.get("/read_ingresos", response_class=HTMLResponse, tags=["Cobros"])
async def mostrar_pagos_pendientes(
    request: Request, 
    mes: str = None,  # Recibe un parámetro en formato YYYY-MM
    db: Session = Depends(get_db)
):
    """
    Muestra los pagos pendientes para el mes y año especificados, 
    actualizando las fechas según corresponda.
    """
    try:
        # Obtener mes y año actuales si no se especifica
        if not mes:
            anio = datetime.now().year
            mes_num = datetime.now().month
        else:
            anio, mes_num = map(int, mes.split("-"))

        # Generar las fechas de inicio y fin del mes solicitado
        fecha_inicio = date(anio, mes_num, 1)
        fecha_fin = (fecha_inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        print(f"Fecha inicio generada: {fecha_inicio}")
        print(f"Fecha fin generada: {fecha_fin}")

        # Consultar los pagos pendientes para el rango de fechas
        pagos = crud.obtener_pagos_pendientes(db, fecha_inicio, fecha_fin)

        
        pagos_actualizados = [
            {
                "nombre": pago[0],
                "apellido": pago[1],
                "combo": pago[2],
                "precio": pago[3],
                "fecha_programada": pago[4].strftime("%Y-%m-%d") if pago[4] else None,
                "fecha_pago": pago[5].strftime("%Y-%m-%d") if pago[5] else None,
                "estado_pago": pago[6],
                "id_pago": pago[7],
            }
            for pago in pagos
            
        ]
        # Renderizar la plantilla con los datos actualizados
        return templates.TemplateResponse(
            "read_ingresos.html",
            {
                "request": request,
                "cobros": pagos_actualizados,
                "mes_actual": f"{anio}-{mes_num:02d}",
            },
        )
    except Exception as e:
        print(f"Error al mostrar pagos: {e}")
        return JSONResponse(
            status_code=500, 
            content={"message": "Ocurrió un error al mostrar los pagos"}
        )






#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//


#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
from datetime import date, timedelta


@router.get("/cobros/actuales", response_class=JSONResponse, tags=["Cobros"])
async def cobros_actuales(mes: str, db: Session = Depends(get_db)):
    try:
        # Extraer año y mes del parámetro `mes` (formato esperado: 'YYYY-MM')
        anio, mes_num = map(int, mes.split("-"))

        # Generar las fechas de inicio y fin
        fecha_inicio = date(anio, mes_num, 1)
        fecha_fin = (fecha_inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        # Depuración
        print(f"Fecha inicio: {fecha_inicio}, Fecha fin: {fecha_fin}")

        # Consultar los cobros en el rango
        cobros = crud.obtener_pagos_pendientes(db, fecha_inicio, fecha_fin)

        cobros_json = [
        {
            "id_pago": c[7],  # Índice del id_pago en la consulta
            "nombre": c[0],
            "apellido": c[1],
            "combo": c[2],
            "precio": c[3],
            "fecha_programada": c[4].strftime("%Y-%m-%d"),
            "fecha_pago": c[5].strftime("%Y-%m-%d") if c[5] else None,
            "estado_pago": c[6],
        }
        for c in cobros
    ]
        return {"success": True, "data": cobros_json}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"success": False, "message": "Error al obtener cobros."}








#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

@router.post("/procesar_actualizacion_pago", tags=["Cobros"])
async def procesar_actualizacion_pago(
    id_pago: int = Form(...),
    fecha_pago: str = Form(...),
    estado_pago: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Actualizar el pago en la base de datos
        pago = db.query(models.Pago).filter(models.Pago.id_pago == id_pago).first()

        if not pago:
            return JSONResponse(
                status_code=404,
                content={"message": f"No se encontró el pago con ID {id_pago}"}
            )

        # Actualizar campos
        pago.fecha_pago = fecha_pago
        pago.estado_pago = estado_pago
        db.commit()

        return RedirectResponse(url="/read_ingresos", status_code=303)
    except Exception as e:
        print(f"Error al actualizar pago: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Error al actualizar el pago"}
        )
#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//
@router.get("/actualizar_pago/{id_pago}", response_class=HTMLResponse, tags=["Cobros"])
async def mostrar_actualizar_pago(id_pago: int, request: Request, db: Session = Depends(get_db)):
    try:
        # Obtener los datos del pago por ID
        pago = (
            db.query(
                models.Pago.id_pago,
                models.Socio.nombre,
                models.Socio.apellido,
                models.Plan.nombre_plan.label("combo"),
                models.Plan.precio,
                models.Pago.fecha_programada,
                models.Pago.fecha_pago,
                models.Pago.estado_pago,
            )
            .join(models.Socio, models.Pago.id_socio == models.Socio.id_socio)
            .join(models.Plan, models.Socio.id_plan == models.Plan.id_plan)
            .filter(models.Pago.id_pago == id_pago)
            .first()
        )

        if not pago:
            return JSONResponse(
                status_code=404,
                content={"message": f"No se encontró el pago con ID {id_pago}"}
            )

        # Renderizar el template con los datos del pago
        return templates.TemplateResponse(
            "actualizar_pago.html",
            {
                "request": request,
                "pago": {
                    "id_pago": pago.id_pago,
                    "nombre": pago.nombre,
                    "apellido": pago.apellido,
                    "combo": pago.combo,
                    "precio": pago.precio,
                    "fecha_programada": pago.fecha_programada.strftime("%Y-%m-%d"),
                    "fecha_pago": pago.fecha_pago.strftime("%Y-%m-%d") if pago.fecha_pago else "",
                    "estado_pago": pago.estado_pago,
                },
            },
        )
    except Exception as e:
        print(f"Error al mostrar formulario de actualización: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Error al mostrar el formulario de actualización"}
        )