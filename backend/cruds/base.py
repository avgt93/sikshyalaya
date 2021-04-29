from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.db import Base
from core.permission.permission import check_permission
from models import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    # @check_permission
    def get(
        self,
        db: Session,
        id: Any,
        # req_user: User
    ) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_self(
        self,
        db: Session,
        # req_user: User
    ) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == req_user.id).first()

    # @check_permission
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        # req_user: User,
    ) -> List[ModelType]:
        if limit == -1:
            return db.query(self.model).offset(skip).all()
        else:
            return db.query(self.model).offset(skip).limit(limit).all()

    # @check_permission
    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
        # req_user: User
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # @check_permission
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        # req_user: User,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(
        self,
        db: Session,
        *,
        id: int,
        # req_user: User
    ) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj