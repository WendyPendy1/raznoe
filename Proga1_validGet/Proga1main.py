from sqlalchemy.dialects.postgresql import UUID
import pydantic, requests, sqlalchemy, pprint
from pydantic.types import List

link = "https://gorest.co.in/public/v1/users"

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("users", sqlalchemy.Integer, primary_key=True)
)

def func1():
    zapr = requests.get(link)
    zapr_json = zapr.json()['data']
    print(pprint.pprint(zapr_json))

    class Us(pydantic.BaseModel):
        email: str
        gender: str
        id: int
        name: str
        status: str

    map=[]
    # парсинг джейсона по мапингу списка
    for item in zapr_json:
        obj_cl=Us(**item)
        map.append(obj_cl)
        print(obj_cl.id+10)
        # код ниже здесь не имеет смысла, потому что parse_obj хорошо
        # работает при поступающих словарях написанных в ручную
        k=Us.parse_obj(obj_cl)
        if k.name == 'Anasooya Marar':
            print(k.id)
            print(k.id+10)

    for item in map:
        if item.gender=="male":
            print(item.name)

#парсинг джейсона через parse_obj()
def func2():
    class model1(pydantic.BaseModel):
        id: int
        name: str
        email: str
        gender: str
        status: str

    class players(pydantic.BaseModel):
        Game: int
        title: str
        Players: List[model1]

    data = {
        "Game": 5,
        "title" : "Piraty",
        "Players":[{
            "id": 5,
            "name": "coldzera",
            "email": "df@df",
            "gender": "male",
            "status": "active"
        },
        {
            "id": 5,
            "name": "coldzera",
            "email": "df@df",
            "gender": "male",
            "status": "active"
        },
        {
            "id": 5,
            "name": "coldzera",
            "email": "df@df",
            "gender": "male",
            "status": "active"
        }]
    }
    obj=players.parse_obj(data)

    for item in obj.Players:
        item.id +=2
    print(obj)

    schema = players.schema()
    print(schema)
func2()






