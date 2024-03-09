import pinecone
import os
# from dotenv import load_dotenv
from pinecone import Pinecone

# load_dotenv()
# base_filepath = os.getenv('BASE_FILEPATH')
# pinecone_key= os.getenv('PINECONE_API_KEY')
# pinecone_env= os.getenv('PINECONE_ENV')
# pinecone_index_name= os.getenv('PINECONE_INDEX_NAME')

base_filepath = "C:\\Users\\jayanth.kappala\\Downloads\\Semantic_Search_Accelerator-main\\Semantic_Search_Accelerator-main\\"
pinecone_key= "2760a8de-3581-47d2-a823-83624abb563d"
pinecone_env= "gcp-starter"
pinecone_index_name= "semantic-search-pinecone"


pc = Pinecone(api_key=pinecone_key)

# p_index = pc.Index(index_name=pinecone_index_name)
index = pc.Index("semantic-search-pinecone")

# Function to query Pinecone index using cosine similarity
def query_pinecone_index(model,query_text,top_k):
    print("Inside query method : ")
    query_embedding = model.embed_query(query_text)
    return index.query(vector=query_embedding, top_k=top_k, include_metadata=True,namespace="")

def clearingTheIndex():
    print(index.delete(index=pinecone_index_name,deleteAll=True, namespace=''))
    print("After deletion : "+str(index.describe_index_stats()))

def upsertingTheData(ids,embeddings,metadatas):
    index.upsert(vectors=zip(ids,embeddings,metadatas))
    print("After upserting : "+str(index.describe_index_stats()))
