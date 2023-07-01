from core import db

def create(cls: db.Model, data:dict) -> db.Model:
    inst = cls(**data)
    db.session.add(inst)
    db.session.commit()
    return inst