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

# Esquemas para Socio
class SocioBase(BaseModel):
    nombre: str
    apellido: str
    dni: int
    fecha_nacimiento: Optional[date]
    genero: Optional[str]
    email: Optional[EmailStr]
    telefono: Optional[str]
    direccion: Optional[str]
    fecha_ingreso: Optional[date]
    id_plan: Optional[int]
    id_plan_social: Optional[int]

class SocioCreate(SocioBase):
    pass

class SocioUpdate(SocioBase):
    nombre: Optional[str]
    apellido: Optional[str]
    dni: Optional[int]
    fecha_nacimiento: Optional[str]
    genero: Optional[str]
    email: Optional[str]
    telefono: Optional[str]
    direccion: Optional[str]
    fecha_ingreso: Optional[str]
    id_plan: Optional[int]
    id_plan_social: Optional[int]

class Socio(SocioBase):
    id_socio: int

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