from schemas.foo import FooItemCreate
from utils.app_exceptions import AppException
from models.foo import FooItem
from utils.service_result import ServiceResult
import openai
openai.organization = "org-deLI2GByWsNO21i26Eycocxs"
openai.api_key = "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"
MODEL = "text-similarity-babbage-001"

class GPT3Service():

    def get_engines():
        return openai.Engine.list
    
    def get_embedding(query):
        return openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
    
    def get_batch_embeddings(batch):
        res = openai.Embedding.create(input=batch, engine=MODEL)
        embeds = [record['embedding'] for record in res['data']]
        return embeds





