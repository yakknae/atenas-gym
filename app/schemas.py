from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date,time

#=============================== C O M B O S ================================================
# Esquemas para ComboPlan
class PlanBase(BaseModel):
    nombre_plan: str
    dias: int
    descripcion: Optional[str]
    precio: float

class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    pass

class Plan(PlanBase):
    id_plan: int

class Config:
     from_attributes = True

#=============================== PLANES S O C I A L E S ================================================

# Esquemas para PlanSocial
class PlanSocialBase(BaseModel):
    nombre_plan_social: str

class PlanSocialCreate(PlanSocialBase):
    pass

class PlanSocialUpdate(PlanSocialBase):
    pass

class PlanSocial(PlanSocialBase):
    id_plan_social: int


class Config:
     from_attributes = True

#=============================== S O C I O S ================================================

class SocioBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_plan: Optional[int] = None
    id_plan_social: Optional[int] = None

# Esquema para crear un nuevo socio
class SocioCreate(BaseModel):
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_plan: Optional[int] = None
    id_plan_social: Optional[int] = None

# Esquema para actualizar un socio existente
class SocioUpdate(BaseModel):  # No es necesario heredar de SocioBase si se definen todos los campos como opcionales
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[int] = None
    fecha_nacimiento: Optional[date] = None  # Cambiado a `date` para consistencia
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_plan: Optional[int] = None
    id_plan_social: Optional[int] = None

# Esquema para representar un socio completo (lectura)
class Socio(SocioBase):
    id_socio: int  # Este campo es de solo lectura y debe estar presente en las respuestas

    class Config:
        from_attributes = True


#=============================== A S I S T E N C I A S ================================================
# Esquema base para la asistencia
class AsistenciaBase(BaseModel):
    socio_id: int
    fecha: date
    hora: time 

class AsistenciaCreate(AsistenciaBase):
    pass

class AsistenciaUpdate(AsistenciaBase):
    pass

class Asistencia(AsistenciaBase):
    id: int
    socio: SocioBase


class Config:
     from_attributes = True

#=============================== L O G I N ================================================
# Esquema base para la asistencia
class LoginBase(BaseModel):
    name:str
    password:str

class LoginCreate(LoginBase):
    pass

class LoginUpdate(LoginBase):
    pass

class Login(LoginBase):
    id: int


class Config:
     from_attributes = True

#=============================== P A G O S ================================================
class PagoBase(BaseModel):
    id_socio: int
    id_plan: int
    fecha_programada: date
    fecha_pago: Optional[date] = None
    estado_pago: Optional[str] = "Pendiente"
    mes_correspondiente: date

class PagoCreate(PagoBase):
    pass

class PagoUpdate(PagoBase):
    pass

class Pago(PagoBase):
    id_pago: int 

    class Config:
        from_attributes = True


#===============================================================================
class Respuesta(BaseModel):
    success: bool
    message: str = None


#===============================================================================

