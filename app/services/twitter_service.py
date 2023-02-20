import datetime
from typing import Any

from sqlalchemy import select, Result
from config.twitter import twitterApi
from api.twitter.schema import TwitterMentionDTO, TwitterUser
import tweepy

from db.models.external_system_user_details import ExternalSystemUserDetailsModel
from services.ExternalUserDetailsService import ExternalUserDetailsService, ExternalUserDetailsCRUD
from db.models.mention_model import MentionModel
from services.main import BaseService, BaseCRUD


class TwitterService(BaseService):

    def get_new_twitter_mentions(self, company_name, company_twitter_handle):
        """

        Args:
            company_name: the name of the company
            company_twitter_handle: the companies twitter handle

        Returns: Mentions of the company from twittter

        """
        query = self.build_query(company_name, company_twitter_handle)
        tweets = tweepy.Cursor(twitterApi.search_tweets, q=query, lang="en", tweet_mode="extended", count=50).items(50)
        new_mentions = [
            self.build_mentionDTO_from_tweet(tweet) for tweet in tweets
        ]  # probably redundant building this here.
        for mention in new_mentions:
            user_external_id = mention.user.external_id
            user = ExternalUserDetailsCRUD(self.db).create_or_update(ExternalSystemUserDetailsModel,
                                                                     reference_id=user_external_id,
                                                                     external_id=user_external_id,
                                                                     source_system_id=1,
                                                                     screen_name=mention.user.screen_name,
                                                                     description=mention.user.description,
                                                                     profile_image_url=mention.user.profile_image_url
                                                                     )  # TODO - Dont pass in ref id twice
            MentionsCrud(self.db).create_not_exists_external_id(MentionModel,
                                                                reference_id=mention.id,
                                                                external_id=mention.id,
                                                                source_system_id=1,
                                                                full_text=mention.full_text,
                                                                external_user_id=user.id
                                                                )  # TODO - Dont pass in ref id twice
        return new_mentions

    def get_new_mentions(self):
        mentions = MentionsCrud(self.db).get_mentions()
        mentionDTOs = [
           self.build_mentionDTO(mention) for mention in mentions
        ]
        return mentionDTOs

    @staticmethod
    def build_query(company_name, company_twitter_handle):
        query = "-from:{handle} -is:retweet {name} OR #{name}".format(handle=company_twitter_handle, name=company_name)
        return query

    @staticmethod
    def build_mentionDTO_from_tweet(tweet) -> TwitterMentionDTO:
        return TwitterMentionDTO(
            created_at=tweet.created_at,
            id=tweet.id_str,
            full_text=tweet.full_text,
            metadata=tweet.metadata,
            user=TwitterUser(
                external_id=tweet.user.id_str,
                source_id=1,
                screen_name=tweet.user.screen_name,
                description=tweet.user.description,
                profile_image_url=tweet.user.profile_image_url
            )
        )

    @staticmethod
    def build_mentionDTO(mention) -> TwitterMentionDTO:
        return TwitterMentionDTO(
            created_at="not working",
            id=mention.MentionModel.external_id,
            full_text=mention.MentionModel.full_text,
            metadata={
                'source_id': mention.MentionModel.source_system.id,
                'source_name': mention.MentionModel.source_system.system_name,
            },
            user=TwitterUser(
                external_id=mention.MentionModel.external_user.external_id,
                source_id=mention.MentionModel.external_user.source_system_id,
                screen_name=mention.MentionModel.external_user.screen_name,
                description=mention.MentionModel.external_user.description,
                profile_image_url=mention.MentionModel.external_user.profile_image_url
            )
        )


class MentionsCrud(BaseCRUD):
    def get_mentions(self) -> Result[MentionModel]:
        """
        Returns: Mentions that are marked as new in the db
        """
        stmt = select(MentionModel).where(MentionModel.new == True)
        return self.db.execute(stmt)


