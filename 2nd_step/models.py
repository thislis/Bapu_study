from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Menu(Base):
    __tablename__ = "menus" 

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    meal_type = Column(String, index=True)
    rest_name = Column(String, index=True)
    menu_name = Column(String, index=True)