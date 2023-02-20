from typing import List

from sqlalchemy import null, select

from api.product_hunt.schema import ProductHuntPostResponse, Edge, Post

import requests

from db.models.mention_model import MentionModel
from db.models.external_system_user_details import ExternalSystemUserDetailsModel
from services.main import BaseService, BaseCRUD

access_token = "GT6Vx3FsGNcjI8BifASZiRltohnnWFoEeUoRtVtAImM"
ph_url = "https://api.producthunt.com/v2/api/graphql"
headers = {"Authorization": f"Bearer {access_token}"}


class ProductHuntService(BaseService):

    def get_post_comments(self, url: str):
        query = self.build_query(url)
        request = requests.post(ph_url, json=query, headers=headers)

        if request.status_code == 200:
            product_hunt_post = ProductHuntPostResponse.parse_obj(request.json())
            new_mentions = self.build_new_mentions(product_hunt_post.data.post)
            new_users = self.build_new_users(product_hunt_post.data.post.comments)

            ProductHuntCrud(self.db).create_user_not_exists_external_id(new_users)
            ProductHuntCrud(self.db).create_mention_not_exists_external_id(new_mentions)

        else:
            raise Exception(f"Query failed to run with a {request.status_code}.")

    @staticmethod
    def build_query(url: str):
        split_url = url.split("/")
        slug = split_url[-1]  # TODO - find a more robust way to handle this
        get_post_comments_query = """
          query MyQuery($slug: String!) {
              post(slug: $slug) {
                  id
                  description
                  commentsCount
                  comments {
                    edges {
                      node {
                        id
                        body
                        createdAt
                        user {
                          id
                          username
                          profileImage
                        }
                      }
                    }
                  }
               }
          }"""
        variables = {"slug": slug}

        payload = {
            "query": get_post_comments_query,
            "variables": variables
        }
        return payload

    @staticmethod
    def build_new_mentions(post):
        new_mentions = [MentionModel(
            external_id=comment.node.id,
            source_system_id=2,
            full_text=comment.node.body,
            external_user_id=comment.node.user.id
        ) for comment in post.comments.edges]
        return new_mentions

    @staticmethod
    def build_new_users(comments):
        new_users = [ExternalSystemUserDetailsModel(
            external_id=comment.node.user.id,
            source_system_id=2,
            screen_name=comment.node.user.username,
            description=None,
            profile_image_url=comment.node.user.profileImage,
        ) for comment in comments.edges]
        return new_users


class ProductHuntCrud(BaseCRUD):
    def create_mention_not_exists_external_id(self, mentions: List[MentionModel]):
        for mention in mentions:
            query = select(MentionModel).filter_by(external_id=mention.external_id)
            instance = self.db.execute(query).scalar_one_or_none()
            if instance is None:
                self.db.add(mention)
                self.db.commit()

    def create_user_not_exists_external_id(self, users: List[ExternalSystemUserDetailsModel]):
        for user in users:
            query = select(ExternalSystemUserDetailsModel).filter_by(external_id=user.external_id)
            instance = self.db.execute(query).scalar_one_or_none()
            if instance is None:
                self.db.add(user)
                self.db.commit()
