from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas, models
from fastapi.templating import Jinja2Templates
import logging
from sqlalchemy.exc import IntegrityError
from typing import Dict
import json
from datetime import date



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
@router.get("/crear_socio", response_class=HTMLResponse)
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

# Crear un socio (POST)
@router.post("/crear_socio", response_class=HTMLResponse)
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
    id_plan: int = Form(None),
    id_plan_social: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        socio_data = schemas.SocioCreate(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            email=email,
            telefono=telefono,
            direccion=direccion,
            id_plan=id_plan,
            id_plan_social=id_plan_social,
        )
        crud.create_socio(db, socio_data)
        message = "Socio creado exitosamente."
    except IntegrityError as e:
        message = f"Error al crear el socio: {str(e)}"
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

# Actualizar un socio (POST)
@router.post("/socios/{socio_id}/actualizar", response_class=HTMLResponse, tags=["Socios"])
async def actualizar_socio(
    request: Request,
    socio_id: int,
    nombre: str = Form(None),
    apellido: str = Form(None),
    dni: int = Form(None),
    fecha_nacimiento: str = Form(None),
    genero: str = Form(None),
    email: str = Form(None),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db),
      
):
    try:
        socio_actualizado = crud.update_socio(
            db,
            socio_id,
            schemas.SocioUpdate(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                email=email,
                telefono=telefono,
                direccion=direccion
            )
        )
        if socio_actualizado is None:
            raise HTTPException(status_code=404, detail="Socio no encontrado")
        message = "Socio actualizado exitosamente"
    except Exception as e:
        message = f"Error al actualizar el socio: {str(e)}"
    
    return templates.TemplateResponse("read_socios.html", {
        "request": request,
        "message": message
    })

#//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//--//

# Eliminar un socio (POST)
@router.post("/socios/{socio_id}/eliminar", response_class=HTMLResponse, tags=["Socios"])
async def delete_socio(request: Request, socio_id: int, db: Session = Depends(get_db)):  # Agrega 'request'
    try:
        result = crud.delete_socio(db, socio_id)
        if result.get("status") == "success":
            message = "Socio eliminado exitosamente"
        else:
            message = "Error al eliminar el socio"
    except Exception as e:
        message = f"Error: {str(e)}"
    
    return templates.TemplateResponse("read_socios.html", {
        "request": request, 
        "message": message
    })
#=============================== PLANES S O C I A L E S ================================================

# Mostrar formulario para crear un plan social
@router.get("/crear_plan_social", response_class=HTMLResponse, tags=["Planes Sociales"])
async def show_create_plan_social_form(request: Request):
    return templates.TemplateResponse("crear_plan_social.html", {"request": request})

# Crear un nuevo plan social
@router.post("/crear_plan_social", response_class=HTMLResponse, tags=["Planes Sociales"])
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

# Leer todos los planes sociales
@router.get("/read_planes_sociales", response_class=HTMLResponse)
async def read_planes_sociales(request: Request, db: Session = Depends(get_db)):
    planes_sociales = crud.get_all_planes_sociales(db)  # Cambiado a get_all_planes_sociales
    return templates.TemplateResponse("read_planes_sociales.html", {
        "request": request,
        "planes_sociales": planes_sociales
    })

# Obtener un plan social por ID
@router.get("/planes_sociales/{plan_social_id}", response_class=HTMLResponse, tags=["Planes Sociales"])
async def read_plan_social(plan_social_id: int, db: Session = Depends(get_db)):
    plan_social = crud.get_plan_social(db, plan_social_id)
    if plan_social is None:
        raise HTTPException(status_code=404, detail="Plan social no encontrado")
    return templates.TemplateResponse("detalle_plan_social.html", {
        "plan_social": plan_social
    })

# Actualizar un plan social
@router.post("/planes_sociales/{plan_social_id}/actualizar", response_class=HTMLResponse, tags=["Planes Sociales"])
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

# Eliminar un plan social
@router.post("/planes_sociales/{plan_social_id}/eliminar", tags=["Planes Sociales"])
async def delete_plan_social(plan_social_id: int, db: Session = Depends(get_db)):
    result = crud.delete_plan_social(db, plan_social_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return {"message": "Plan social eliminado exitosamente"}

#=============================== C O M B O S ================================================
# Mostrar formulario para crear un plan
@router.get("/crear_plan", response_class=HTMLResponse, tags=["Plan combo"])
async def show_create_plan_form(request: Request):
    return templates.TemplateResponse("crear_plan.html", {"request": request})

@router.post("/crear_plan", response_class=HTMLResponse, tags=["Plan combo"])
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

# Leer todos los planes
@router.get("/read_combos", response_class=HTMLResponse)
async def read_planes(request: Request, db: Session = Depends(get_db)):
    planes = crud.get_all_planes(db)
    print(planes)  # Verificar en la consola si se obtienen los datos correctamente
    return templates.TemplateResponse("read_combos.html", {
        "request": request,
        "combos": planes
    })

# Obtener un plan por ID (detalles)
@router.get("/planes/{plan_id}", response_class=HTMLResponse)
async def read_plan(plan_id: int, request: Request, db: Session = Depends(get_db)):
    plan = crud.get_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return templates.TemplateResponse("detalle_plan.html", {
        "request": request,
        "plan": plan
    })

# Actualizar un plan
@router.post("/planes/{plan_id}/actualizar", response_class=HTMLResponse)
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

# Eliminar un plan
@router.post("/planes/{plan_id}/eliminar", status_code=200)
async def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    result = crud.delete_plan(db, plan_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": result["message"]}



#=============================== A S I S T E N C I A S ================================================
@router.post("/registrar_asistencia", tags=["Asistencias"])
async def registrar_asistencia(
    asistencias: Dict[int, bool], 
    db: Session = Depends(get_db)
):
    """
    Registra asistencias para los socios.
    :param asistencias: Diccionario {socio_id: asistencia (True/False)}
    :param db: Sesión de la base de datos
    """
    try:
        result = crud.registrar_asistencia(db, asistencias)
        return {"message": result["message"]}
    except Exception as e:
        return {"error": str(e)}

@router.get("/asistencias", response_class=HTMLResponse, tags=["Asistencias"])
async def mostrar_asistencias(
    request: Request,
    year: int = date.today().year,
    month: int = date.today().month,
    db: Session = Depends(get_db),
):
    datos = crud.obtener_asistencias_por_mes(db, year, month)
    años = list(range(2020, 2031))
    return templates.TemplateResponse(
        "asistencias.html",
        {
            "request": request,
            "datos": datos,
            "selected_year": year,
            "selected_month": month,
            "años": años,
        },
    )


@router.post("/asistencias", response_class=HTMLResponse, tags=["Asistencias"])
async def guardar_asistencias_endpoint(
    request: Request,
    year: int = Form(...),
    month: int = Form(...),
    asistencias: str = Form(...),  # JSON string enviado desde el formulario
    db: Session = Depends(get_db)
):
    """
    Guarda las asistencias enviadas desde un formulario.
    :param year: Año de las asistencias.
    :param month: Mes de las asistencias.
    :param asistencias: Cadena JSON con los datos de las asistencias.
    """
    try:
        # Parseo seguro del JSON
        asistencias_lista = json.loads(asistencias)
        crud.guardar_asistencias(db, asistencias_lista, year, month)
        message = "Asistencias guardadas correctamente."
    except json.JSONDecodeError:
        message = "Error al decodificar las asistencias. Asegúrate de enviar un JSON válido."
    except Exception as e:
        message = f"Error al guardar asistencias: {str(e)}"

    # Cargar los datos nuevamente después de intentar guardar
    datos = crud.obtener_asistencias_por_mes(db, year, month)
    return templates.TemplateResponse("asistencias.html", {
        "request": request,
        "datos": datos,
        "message": message,
        "year": year,
        "month": month,
    })

#=============================== L O G I N ================================================

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Endpoint de autenticación
@router.post("/login")
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
    
@router.get("/index")
def show_index(request: Request):
    authenticated = request.cookies.get("authenticated")
    if authenticated == "true":
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return RedirectResponse(url="/")