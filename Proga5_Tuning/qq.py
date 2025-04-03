import uvicorn
from sqlalchemy import create_engine, Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends, Form, Query, Body
from fastapi.responses import FileResponse

Base=declarative_base()

link="postgresql+psycopg2://postgres:user@localhost:5432/Exp"
engine=create_engine(url=link, echo=True)
SessionLoc=sessionmaker(bind=engine, autoflush=False, autocommit=False)


class table(Base):
	__tablename__="table_users"
	id=Column(Integer, primary_key=True)
	name=Column(String, nullable=False)
	passw=Column(String, nullable=False)

class table_auth(Base):
	__tablename__="table_auth"
	id=Column(Integer, primary_key=True)
	login=Column(String, nullable=False)
	passw=Column(String, nullable=True)

Base.metadata.create_all(engine)

def get_bd():
	bd=SessionLoc()
	try:
		yield bd
	finally:
		bd.close()

class Model(BaseModel):
	id: int
	name: str
	passw: str

app=FastAPI()

m=[]

@app.get("/")
def page():
	return FileResponse('fileAp.html')

@app.post("/create_user")	
def create_user(name: str = Form(...), passw: str = Form(...), bd: Session=Depends(get_bd)):
	user_bd = table(name=name, passw=passw)
	m.append(user_bd)
	bd.add(user_bd)
	bd.commit()
	bd.refresh(user_bd)
	return user_bd

@app.get("/get_user_all")
def get_alluser(bd: Session = Depends(get_bd)):
	users = bd.query(table).all()
	return users

@app.get("/get_user_id")
def sget_userid(vvod_id: int=Query(...), bd: Session = Depends(get_bd)):
	user = bd.query(table).filter(table.id==vvod_id).first()
	if user:
		return {"id: ":user.id, "name: ":user.name}
	else:
		return "Такого id нет"

@app.post("/auth")
def auth(name: str=Form(...), passw: str=Form(...), bd: Session=Depends(get_bd)):
	user = bd.query(table).filter(table.name==name, table.passw==passw).first()
	if user:
		return user
	else:
		return "Not auth"

if __name__=="__main__":
	uvicorn.run(app="qq:app", port=8002, reload=True, host="127.0.0.1")



