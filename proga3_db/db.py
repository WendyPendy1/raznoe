from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, relationship
from config import url
from sqlalchemy import create_engine, Integer, String,Column, ForeignKey


Model = declarative_base()

engine = create_engine(url=url, echo=True)
Session = sessionmaker(engine, autoflush=False, autocommit = False)
session = Session()

class ttt(Model):
    __tablename__="ttt"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    dl = relationship("nasled")

class nasled(Model):
    __tablename__="nasled"
    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    ttt_id=Column(Integer, ForeignKey('ttt.id'))

class new_table(Model):
    __tablename__="new_table"
    id=Column(Integer,primary_key=True)
    col1=Column(Integer, nullable=False)
    col2=Column(String, autoincrement=True)

Model.metadata.create_all(engine)

def insert_data(Imya: str):
    ww=ttt(username = Imya)
    session.add(ww)
    session.commit()
    session.close()

async def insert_data2(Imya:str):
    with session as ses:
        ww=ttt(username=Imya)
        ses.add(ww)
        await ses.commit()

def k_input():
    k=int(input())
    for i in range(0,k):
        name=input()
        insert_data(name)

def get_data():
    with session as ses:
        select=ses.query(ttt).all()
        for p in select:
            print(p.id, p.username)