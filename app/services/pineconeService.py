import pinecone

pinecone.init(
    api_key="269823e3-1327-47ab-a695-27f80871679f",
    environment="us-west1-gcp"
)

class PineConeService():

    def get_or_create_index(index:str, **kwargs):
        if index not in pinecone.list_indexes():
            pinecone.create_index(index, dimension=kwargs.get("dim",None))
        return pinecone.Index(index)