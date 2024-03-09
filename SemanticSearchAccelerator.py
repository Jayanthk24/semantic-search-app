from ibm_cloud_sdk_core import IAMTokenManager
import requests
from uuid import uuid4
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import requests
import os 
from Database import query_pinecone_index, index

# Load the environment variables
database = "Pinecone"


project_id="5bd23f2e-c88b-42f9-b4f1-f944ac855038"
endpoint_url="https://us-south.ml.cloud.ibm.com"
api_key="izlDY51M0CoWm3W382XRBrXAJYKsCql4QTBTDTZYmQ"

# Function to genearte access token for IBM 
access_token = IAMTokenManager(
    apikey = api_key,
    url = "https://iam.cloud.ibm.com/identity/token"
).get_token()
 
def generate(input):
    parameters = {
         "decoding_method": "greedy",
         "random_seed": 33,
         "repetition_penalty":1,
         "min_new_tokens": 50,
         "max_new_tokens": 300
        }
    # model_id = "google/flan-t5-xxl"
    model_id = "meta-llama/llama-2-70b-chat"
    wml_url = f"{endpoint_url}/ml/v1-beta/generation/text?version=2023-05-28"
    Headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    data = {
            "model_id": model_id,
            "input": input,
            "parameters": parameters,
            "project_id": project_id
        }
    response = requests.post(wml_url, json=data, headers=Headers, verify=False)
    if response.status_code == 200:
        print("Responseeee: ",response.json())
        return response.json()["results"][0]
    else:
        return response.text

# main method
def query_vectordb(user_question):
    
    model_name = "all-MiniLM-L6-v2"
    model = SentenceTransformerEmbeddings(model_name=model_name)          
   
    try:
        top_3_search_results_text=""
        top_k_results = 3
              
        if database == "Pinecone":
            stats = index.describe_index_stats()
            total_vector_count = stats['total_vector_count']
            top_k_results = 3
            print("total_vector_count: ",total_vector_count)
            if total_vector_count != 0:
                result_ids = query_pinecone_index(model,user_question,top_k_results)
                print("Results_ids", result_ids['matches'])
                # Print the results
                for i,idx in enumerate(result_ids['matches']):
                    text=idx['metadata']['text'].strip().replace('\n', ' ').replace('\r', '')
                    top_3_search_results_text = top_3_search_results_text+text
                    print("Chunck Text "+str(i)+" : "+text)
                    print("Similarity score : ",end="")
                    print(idx['score'])
            else:
                raise Exception("No data found in the Pinecone index")      
            
            prompt = f"""Context: You are a virtual assistant with access to a comprehensive document. Your task is to provide accurate responses to specific queries based on the content of the document.
            Documents : {top_3_search_results_text}
            Question: {user_question}
            Response Format: Please provide relevant answer to the Question based on the information provided in the Documents.
            Answer the question as 'I don't know.' If you can't find the answer from the above data. Also, please use professional tone to answer the query. Please end your response properly without leaving statements incomplete."""

            response = generate(prompt) 
            if response.__contains__('generated_text') :
                return response['generated_text']
            else:
                return response
           
    except Exception as e:    
        raise Exception(f"Exception occured while processing the request : {e}")
    
