import uvicorn
from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session, declarative_base, relationship
from sqlalchemy import Column, Integer, String, create_engine

Model = declarative_base()
url = f'postgresql+psycopg://postgres:user@localhost:5432/Exp'
engine=create_engine(url = url, echo=True)
def get_db():
    session=Session(bind=engine, autoflush=False, autocommit=False)
    return session

class table1(Model):
    __tablename__="table1"
    id=Column(Integer, primary_key=True)
    username=Column(String, nullable=False)
    balance=Column(Integer)

class table2(Model):
    __tablename__="table2"
    id=Column(Integer, primary_key=True)
    username=Column(String, nullable=False)
    balance=Column(Integer)

Model.metadata.create_all(engine)

# def get_db():
#     db=session()
#     try:
#         yield db
#     finally:
#         db.close()

app=FastAPI()
router=APIRouter()

@router.post("/money1")
def money1(name:str, balance:int, db=Depends(get_db)):
    wsx=table1(username=name, balance=balance)
    db.add(wsx)
    db.commit()
    db.refresh(wsx)
    return wsx

@router.post("/money2")
def money2(name: str, balance:int, db=Depends(get_db)):
    wsx=table2(username=name, balance=balance)
    db.add(wsx)
    db.commit()
    db.refresh(wsx)
    return wsx

@router.post("/transact")
def transact1(username1: str, username2:str, money:int, db=Depends(get_db)):
    t1=db.query(table1).filter(table1.username==username1).first()
    t2=db.query(table2).filter(table2.username==username2).first()
    if t1 and t2:
        t1.balance=t1.balance-money
        t2.balance=t2.balance+money
        try:
            db.commit()
            return {"all good"}
        except Exception as e:
            db.rollback()
            return {"no transact"}

@router.post("/filter")
def filter(id:int=None, name: str=None, db=Depends(get_db)):
    if id:
        wsx=db.query(table1, table2).join()



app.include_router(router)
if __name__=="__main__":
    uvicorn.run(app=app, port=8005, host="127.0.0.1", reload=True)