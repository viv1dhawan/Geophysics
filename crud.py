# app/crud.py
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserOut
import math

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    from app.auth import get_password_hash
    password = get_password_hash(user.password)
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, user: User, new_password: str):
    from app.auth import get_password_hash 
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user


def wenner_resistivity(potential_difference, current, spacing, number_of_electrodes):
    if number_of_electrodes != 4:
        raise ValueError("Wenner configuration requires exactly 4 electrodes.")
    return 2 * math.pi * spacing * (potential_difference / current)

def schlumberger_resistivity(potential_difference, current, half_distance_current, half_distance_potential, number_of_electrodes):
    if number_of_electrodes != 4:
        raise ValueError("Schlumberger configuration requires exactly 4 electrodes.")
    return (math.pi * (half_distance_current**2) / (2 * half_distance_potential)) * (potential_difference / current)

def dipole_dipole_resistivity(potential_difference, current, spacing_between_dipoles, spacing, total_electrodes):
    if total_electrodes < 4:
        raise ValueError("Dipole-Dipole configuration requires at least 4 electrodes.")
    return math.pi * spacing_between_dipoles * (spacing_between_dipoles + 1) * spacing * (potential_difference / current)

def pole_pole_resistivity(potential_difference, current, spacing, number_of_electrodes):
    if number_of_electrodes != 4:
        raise ValueError("Pole-Pole configuration requires exactly 4 electrodes.")
    return 2 * math.pi * spacing * (potential_difference / current) * number_of_electrodes