import pinecone

pinecone.init(
    api_key="269823e3-1327-47ab-a695-27f80871679f",
    environment="us-west1-gcp"
)


class PineConeService:

    @staticmethod
    def get_or_create_index(index: str, **kwargs):
        if index not in pinecone.list_indexes():
            pinecone.create_index(index, dimension=2048)
        return pinecone.Index(index)

    # currently no limit on batch size, if needed make 100 (recommender limit)
    @staticmethod
    def batch_upsert(ids_batch, embeds, meta, index):
        to_upsert = zip(ids_batch, embeds, meta)
        index.upsert(vectors=list(to_upsert))  # upsert to Pinecone
