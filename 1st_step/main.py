from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

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

class Bap_req(BaseModel):
    rest_name: str
    menus: List[str]

class Menu_Res(BaseModel):
    menus: List[str]


@app.post("/api/set/bap")
async def set_bap(request: Bap_req, db: Session = Depends(get_db)):
    for menu_name in request.menus:
        menu = models.Menu(rest_name=request.rest_name, menu_name=menu_name)
        db.add(menu)
    db.commit()

@app.get("/api/get/bap/{rest_name}", response_model=Menu_Res)
async def get_bap(rest_name: str, db: Session = Depends(get_db)):
    menus = db.query(models.Menu).filter(models.Menu.rest_name == rest_name).all()
    if not menus:
        raise HTTPException(status_code=404, detail="Restaurant doesn't exist")
    menu_names = [menu.menu_name for menu in menus]
    return Menu_Res(menus=menu_names)
