from sqlalchemy import select

from services.main import BaseService, BaseCRUD
from db.models.external_system_user_details import ExternalSystemUserDetailsModel


class ExternalUserDetailsService(BaseService):
    def get_or_create(self,
                      external_id: str,
                      source_id: int,
                      screen_name: str) -> ExternalSystemUserDetailsModel:
        user = ExternalUserDetailsCRUD(self.db).create_or_update(ExternalSystemUserDetailsModel,
                                                              external_id=external_id,
                                                              screen_name=screen_name,
                                                              source_id=source_id)
        return user


class ExternalUserDetailsCRUD(BaseCRUD):
    def create_or_update(self, model, reference_id, **kwargs):
        query = select(model).filter_by(external_id=reference_id)
        user = self.db.execute(query).scalar_one_or_none()
        if user is not None:
            user.screen_name = kwargs.get("screen_name")
            user.description = kwargs.get("description")
            user.profile_image_url = kwargs.get("profile_image_url")
            self.db.flush()
            self.db.commit()
            return user
        else:
            user = model(**kwargs)
            self.db.add(user)
            self.db.commit()
            return user
