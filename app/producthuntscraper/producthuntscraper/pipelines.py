# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sys

from sqlalchemy.ext.declarative import declarative_base
sys.path.append('/app')
# useful for handling different item types with a single interface
from services.main import BaseCRUD
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from db.models.mention_model import MentionModel
from db.models.external_system_user_details import ExternalSystemUserDetailsModel

Base = declarative_base()
class ProducthuntscraperPipeline(BaseCRUD):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        # add User
        user = ExternalSystemUserDetailsModel()
        user.external_id = item["user_id"][0]
        user.source_id = 2
        user.screen_name = item["user_screen_name"][0]
        user.description = None
        user.profile_image_url = item["profile_image_url"][0]

        # add Mention
        mention = MentionModel()
        mention.external_id = item["external_id"][0]
        mention.source_id = 2,
        mention.full_text = item["full_text"][0]
        mention.external_user_id = item["user_id"][0]

        try:
            query = select(ExternalSystemUserDetailsModel).filter_by(external_id=user.external_id)
            exisitngUser = session.execute(query).scalar_one_or_none()
            if exisitngUser is None:
                session.add(user)

            query = select(MentionModel).filter_by(external_id=mention.external_id)
            exisitngMention = session.execute(query).scalar_one_or_none()

            if exisitngMention is None:
                session.add(mention)

            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)
