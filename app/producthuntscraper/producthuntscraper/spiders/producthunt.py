from typing import Generator, Any
from urllib.request import Request

import scrapy
from urllib.parse import urlencode
import json
from scrapy.loader import ItemLoader

from ..items import ProducthuntReviewItem

API = '55ee7a6b8c6644bb0c01cd93ed246548'
product = "mindsdb"

def get_url(url):
    """
     Prepend the scraperapi proxy url to the front of the product hunt URL
     This helps with the bot not getting blocked by PH.
             Parameters:
                     url (str): the product hunt url to scrape.
             Returns:
                     proxy_url (str): the product hunt url prefixed with the scraperapi url
     """
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

#
def get_query(self, cursor):
    """
     Returns the sum of two decimal numbers in binary digits.
             Parameters:
                     cursor (str): The cursor for paginating the graphql endpoint
             Returns:
                     json_data (str): The graphql query, opernation name and variables in JSON form to suit requests.
     """
    json_data = {
        "query": self.query,
        "variables": {
            "slug": product,
            "query": None,
            "reviewsLimit": 100,
            "reviewsOrder": "HELPFUL",
            "includeReviewId": None,
            "rating": "0",
            "reviewsCursor": cursor
        },
        "operationName": "ProductReviewsPage"
    }
    return json_data


class ProducthuntSpider(scrapy.Spider):
    """
    Product Hunt Spider.
    """
    name = "producthunt"
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {'CONCURRENT_REQUESTS_PER_DOMAIN': 5}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_cursor = None
        self.url = f'https://www.producthunt.com/frontend/graphql'

    def start_requests(self):
        """
        Entry point to the scraper.
        get the query based on the cursor and then call self.parse on result
        """
        yield scrapy.Request(get_url(self.url), callback=self.parse, method="POST",
                             body=json.dumps(get_query(self, self.next_cursor)),
                             headers={'content-type': 'application/json'})

    def parse(self, response: {json}) -> Generator[Request, Any, None]:
        """
        parsing of the product hunt product reviews page GraphQL api call.
        build product hunt review item and pass through pipeline.
        """
        data = response.json()
        reviews = data["data"]["product"]["reviews"]
        for edge in reviews["edges"]:
            loader = ItemLoader(item=ProducthuntReviewItem(), selector=edge)
            loader.add_value('external_id', edge["node"]["id"])
            loader.add_value('full_text', edge["node"]["body"])
            loader.add_value('user_id', edge["node"]["user"]['id'])
            loader.add_value('user_screen_name', edge["node"]["user"]['name'])
            loader.add_value('profile_image_url', edge["node"]["user"]["avatarUrl"])
            yield loader.load_item()

        has_next_page_bool = reviews["pageInfo"]["hasNextPage"]
        if has_next_page_bool:
            print("had next cursor getting next page")
            self.next_cursor = reviews["pageInfo"]["endCursor"]
            yield scrapy.Request(get_url(self.url), callback=self.parse, method="POST",
                                 body=json.dumps(get_query(self, self.next_cursor)),
                                 headers={'content-type': 'application/json'})

    # The Graphql Query for the product hunt product reviews page.
    # Some of this may be filtered later
    query = """
          query ProductReviewsPage(
          $slug: String!
          $reviewsLimit: Int!
          $reviewsCursor: String
          $reviewsOrder: ReviewsOrder
          $includeReviewId: ID
          $query: String
          $rating: String
          $tags: [String!]
        ) {
          product(slug: $slug) {
            id
            slug
            name
            reviewsRating
            reviewsCount
            isMaker
            isTrashed
            ...ProductReviewsPageReviewsFeedFragment
          }
        }
        fragment ProductReviewsPageReviewsFeedFragment on Product {
          id
          reviewsCount
          ...ReviewListFragment
          __typename
        }
        fragment ReviewListFragment on Reviewable {
          id
          reviews(
            first: $reviewsLimit
            after: $reviewsCursor
            order: $reviewsOrder
            includeReviewId: $includeReviewId
            query: $query
            rating: $rating
            tags: $tags
          ) {
            edges {
              node {
                id
                sentiment
                comment {
                  id
                  bodyHtml
                  __typename
                }
                ...RatingReviewFragment
                __typename
              }
              __typename
            }
            totalCount
            pageInfo {
              hasNextPage
              endCursor
              __typename
            }
            __typename
          }
          __typename
        }
        fragment RatingReviewFragment on Review {
          id
          rating
          body
          sentiment
          user {
            id
            username
            name
            url
            work {
              id
              jobTitle
              companyName
              product {
                id
                name
                __typename
              }
              __typename
            }
            ...UserImage
            __typename
          }
          comment {
            id
            body
            __typename
          }
          post {
            id
            name
            slug
            __typename
          }
          __typename
        }
        fragment UserImage on User {
          id
          name
          username
          avatarUrl
          __typename
        }
    """
