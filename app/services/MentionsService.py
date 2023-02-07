from select import select

from config.twitter import twitterApi
from api.twitter.schema import TwitterMentionDTO, TwitterUser
import tweepy

from db.models.external_system_user_details import ExternalSystemUserDetailsModel
from services.ExternalUserDetailsService import ExternalUserDetailsService, ExternalUserDetailsCRUD
from db.models.mention_model import MentionModel
from services.main import BaseService, BaseCRUD


class MentionsService(BaseService):

    def get_new_twitter_mentions(self, company_name, company_twitter_handle):
        query = self.build_query(company_name, company_twitter_handle)
        tweets = tweepy.Cursor(twitterApi.search_tweets, q=query, lang="en", tweet_mode="extended", count=10).items(10)
        new_mentions = [
            self.build_new_mention(tweet) for tweet in tweets
        ]  # probably redundant building this here.
        for mention in new_mentions:
            user_external_id = mention.user.external_id
            user = ExternalUserDetailsCRUD(self.db).create_or_update(ExternalSystemUserDetailsModel,
                                                                     reference_id=user_external_id,
                                                                     external_id=user_external_id,
                                                                     source_id=1,
                                                                     screen_name=mention.user.screen_name,
                                                                     description=mention.user.description,
                                                                     profile_image_url=mention.user.profile_image_url
                                                                     ) # TODO - Dont pass in ref id twice
            MentionsCrud(self.db).create_not_exists_external_id(MentionModel,
                                                                reference_id=mention.id,
                                                                external_id=mention.id,
                                                                source_id=1,
                                                                full_text=mention.full_text,
                                                                user_id=user.id
                                                                ) # TODO - Dont pass in ref id twice
        return new_mentions

    @staticmethod
    def build_query(company_name, company_twitter_handle):
        query = "-from:{handle} -is:retweet {name} OR #{name}".format(handle=company_twitter_handle, name=company_name)
        return query

    @staticmethod
    def build_new_mention(tweet) -> TwitterMentionDTO:
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


class MentionsCrud(BaseCRUD):
    pass
