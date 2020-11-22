from sql_helper import SESSION, BASE
from sqlalchemy import Column, String, JSON
from sqlalchemy.orm.attributes import flag_modified


class Stock(BASE):
    __tablename__ = "stok"
    ID = Column(String(3), primary_key=True)
    warna = Column(String, nullable=False)
    ukuran = Column(JSON)

    def __init__(self, ID, warna, ukuran):
        self.ID = ID
        self.warna = warna
        self.ukuran = ukuran


Stock.__table__.create(checkfirst=True)


def get_item(ID: str) -> Stock:
    try:
        boxer = SESSION.query(Stock).get(ID)
        return boxer
    finally:
        SESSION.close()


def update_item(boxer: Stock, ukuran: str, val: int) -> None:
    try:
        boxer.ukuran.get(ukuran)['quantity'] -= val
        flag_modified(boxer, "ukuran")
        SESSION.add(boxer)
        SESSION.commit()
    finally:
        SESSION.close()
