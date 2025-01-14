from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from fastapi.templating import Jinja2Templates
import logging
from sqlalchemy.exc import IntegrityError
from fastapi import Query
from typing import List
from datetime import datetime, timedelta



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
    fecha_ingreso: str = Form(...),
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
            fecha_ingreso=fecha_ingreso,
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
    fecha_ingreso: str = Form(None),
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
                direccion=direccion,
                fecha_ingreso=fecha_ingreso
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
@router.post("/socios/{socio_id}/eliminar", response_class=JSONResponse, tags=["Socios"])
async def delete_socio(request: Request, socio_id: int, db: Session = Depends(get_db)):
    try:
        # Llamada al método de CRUD para eliminar el socio
        result = crud.delete_socio(db, socio_id)
        if result.get("status") == "success":
            return {"success": True, "message": "Socio eliminado exitosamente"}
        else:
            return {"success": False, "message": "Error al eliminar el socio"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
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
    
@router.get("/index" , tags=["Login"])
def show_index(request: Request):
    authenticated = request.cookies.get("authenticated")
    if authenticated == "true":
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return RedirectResponse(url="/login")
    

@router.get("/logout", tags=["Login"])
def logout(response: Response):
    response.delete_cookie("authenticated")
    return RedirectResponse(url="/login")


#=============================== C O B R O S ================================================

@router.get("/read_ingresos", response_class=HTMLResponse , tags=["Cobros"])
async def show_ingresos_semanales(request: Request, db: Session = Depends(get_db)):
    """
    Muestra los socios con cobro pendiente esta semana en el template 'read_ingresos.html'.
    """
    socios = crud.get_socios_cobro_semanal(db)

    if not socios:
        print("No hay datos para mostrar en el template.")
        socios_data = []
    else:
        print(f"Datos enviados al template ({len(socios)} registros):")
        socios_data = []
        for socio in socios:
            fecha_cobro = socio.fecha_ingreso + timedelta(days=30)
            print(f"Nombre: {socio.nombre}, Apellido: {socio.apellido}, Fecha Cobro: {fecha_cobro}")
            socios_data.append({
                "nombre": socio.nombre,
                "apellido": socio.apellido,
                "combo": socio.plan.nombre_plan if socio.plan else "Sin plan",
                "fecha_cobro": fecha_cobro.strftime('%Y-%m-%d')  # Formato amigable
            })

    return templates.TemplateResponse("read_ingresos.html", {
        "request": request,
        "socios": socios_data
    })