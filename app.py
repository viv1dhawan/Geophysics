# app/app.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app import models, schemas, crud, database, auth
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)
# Mount the 'templates' directory to serve HTML templates
templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/reset-password", response_model=schemas.UserOut)
def reset_password(reset_password: schemas.ResetPassword, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=reset_password.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_password(db=db, user=user, new_password=reset_password.new_password)

@app.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: schemas.UserOut = Depends(auth.get_current_user)):
    return current_user

# --------------------------------------Resistivity--------------------------------------------------------------------------------------
@app.post("/wenner_resistivity", response_model=schemas.WennerResponse)
async def calculate_wenner_resistivity(
    request: schemas.WennerRequest, 
    current_user: schemas.TokenData = Depends(auth.get_current_user)
):
    try:
        resistivity = crud.wenner_resistivity(request.potential_difference, request.current, request.spacing, request.number_of_electrodes)
        return schemas.WennerResponse(resistivity=resistivity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/schlumberger_resistivity", response_model=schemas.SchlumbergerResponse)
async def calculate_schlumberger_resistivity(
    request: schemas.SchlumbergerRequest, 
    current_user: schemas.TokenData = Depends(auth.get_current_user)
):
    try:
        resistivity = crud.schlumberger_resistivity(request.potential_difference, request.current, request.half_distance_current, request.half_distance_potential, request.number_of_electrodes)
        return schemas.SchlumbergerResponse(resistivity=resistivity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/dipole_dipole_resistivity", response_model=schemas.DipoleDipoleResponse)
async def calculate_dipole_dipole_resistivity(
    request: schemas.DipoleDipoleRequest, 
    current_user: schemas.TokenData = Depends(auth.get_current_user)
):
    try:
        resistivity = crud.dipole_dipole_resistivity(request.potential_difference, request.current, request.spacing_between_dipoles, request.spacing, request.total_electrodes)
        return schemas.DipoleDipoleResponse(resistivity=resistivity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/pole_pole_resistivity", response_model=schemas.PolePoleResponse)
async def calculate_pole_pole_resistivity(
    request: schemas.PolePoleRequest, 
    current_user: schemas.TokenData = Depends(auth.get_current_user)
):
    try:
        resistivity = crud.pole_pole_resistivity(request.potential_difference, request.current, request.spacing, request.number_of_electrodes)
        return schemas.PolePoleResponse(resistivity=resistivity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))