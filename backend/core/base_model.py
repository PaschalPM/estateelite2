from . import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm.state import InstanceState


class BaseModel:
    id = db.Column(
        db.String(36), default=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    @staticmethod
    def _to_dict(inst):
        data_dict = inst.__dict__.copy()
        print(inst.__dict__)
        for key in inst.__dict__:
            if isinstance(data_dict[key], InstanceState) or key == "password":
                del data_dict[key]
        return data_dict
