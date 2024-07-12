from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

# Models
class Bap_req(BaseModel):
    date: datetime
    meal_type: str
    rest_name: str
    menus: List[str]

class Meal(BaseModel):
    date: datetime
    meal_type: str
    rest_name: str
    menus: List[str]

class Menu_Res(BaseModel):
    menus: List[Meal]

# Controllers
class BapController:
    def __init__(self, db: Session):
        self.db = db

    def set_bap(self, request: Bap_req):
        for menu_name in request.menus:
            menu = models.Menu(date=request.date, meal_type=request.meal_type, rest_name=request.rest_name, menu_name=menu_name)
            self.db.add(menu)
        self.db.commit()

    def get_bap(self, start_time: str, end_time: str):
        menus = self.db.query(models.Menu).filter(models.Menu.date >= start_time and models.Menu.date <= end_time).all()
        if not menus:
            raise HTTPException(status_code=404, detail="밥 없음")
        menu_names = [menu for menu in menus]
        return Menu_Res(menus=menu_names)

# Routes
@app.post("/api/set/bap")
async def set_bap(request: Bap_req, db: Session = Depends(get_db)):
    controller = BapController(db)
    controller.set_bap(request)

@app.get("/api/get/bap/{start_time}/{end_time}", response_model=Menu_Res)
async def get_bap(start_time: str, end_time: str, db: Session = Depends(get_db)):
    controller = BapController(db)
    return controller.get_bap(start_time, end_time)
