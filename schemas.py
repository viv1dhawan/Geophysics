# app/schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    firstname:str
    lastname:str
    email: str
    password: str
    is_active: bool = True


class UserOut(BaseModel):
    id: int
    firstname:str
    lastname:str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class ResetPassword(BaseModel):
    email: str
    new_password: str


class WennerRequest(BaseModel):
    potential_difference: float
    current: float
    spacing: float
    number_of_electrodes: int

class WennerResponse(BaseModel):
    resistivity: float

class SchlumbergerRequest(BaseModel):
    potential_difference: float
    current: float
    half_distance_current: float
    half_distance_potential: float
    number_of_electrodes: int

class SchlumbergerResponse(BaseModel):
    resistivity: float

class DipoleDipoleRequest(BaseModel):
    potential_difference: float
    current: float
    spacing_between_dipoles: int
    spacing: float
    total_electrodes: int

class DipoleDipoleResponse(BaseModel):
    resistivity: float

class PolePoleRequest(BaseModel):
    potential_difference: float
    current: float
    spacing: float
    number_of_electrodes: int

class PolePoleResponse(BaseModel):
    resistivity: float
