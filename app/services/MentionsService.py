from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload

from api.mentions.schema import MentionDTO, MentionUser
from db.models import MentionModel, ExternalSystemUserDetailsModel, SourceSystem
from services.main import BaseService, BaseCRUD


class MentionsService(BaseService):

    def get_new_mentions(self):
        mentions = MentionsCrud(self.db).get_mentions()
        mentionDTOs = [
         self.build_mentionDTO(mention) for mention in mentions
        ]
        return mentionDTOs

    @staticmethod
    def build_mentionDTO(mention) -> MentionDTO:
        user = MentionUser.Builder(validation=False) \
            .external_id(mention.MentionModel.external_user.external_id) \
            .source_id(mention.MentionModel.external_user.source_system_id) \
            .screen_name(mention.MentionModel.external_user.screen_name) \
            .description(mention.MentionModel.external_user.description) \
            .profile_image_url(mention.MentionModel.external_user.profile_image_url) \
            .build()
        mention = MentionDTO.Builder() \
            .created_at("not working") \
            .id(mention.MentionModel.external_id) \
            .full_text(mention.MentionModel.full_text) \
            .metadata({
                'source_id': mention.MentionModel.source_system.id,
                'source_name': mention.MentionModel.source_system.system_name,
            }) \
            .user(user) \
            .build()

        return mention



class MentionsCrud(BaseCRUD):
    def get_mentions(self) -> Result[MentionModel]:
        """
        Returns: Mentions that are marked as new in the db
        """
        stmt = select(MentionModel, ExternalSystemUserDetailsModel, SourceSystem) \
            .join(MentionModel.external_user) \
            .join(MentionModel.source_system).where(MentionModel.new == True)
        return self.db.execute(stmt)
