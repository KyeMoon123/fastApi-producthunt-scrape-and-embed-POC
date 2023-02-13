from sqlalchemy import select
from sqlalchemy.orm import Session


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class BaseService(DBSessionContext):
    pass


class BaseCRUD(DBSessionContext):
    def create_not_exists_external_id(self, model, reference_id, **kwargs):
        query = select(model).filter_by(external_id=reference_id)
        instance = self.db.execute(query).scalar_one_or_none()
        if instance is None:
            instance = model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            return instance
