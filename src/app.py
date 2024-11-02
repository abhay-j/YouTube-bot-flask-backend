from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

model = SentenceTransformer("all-MiniLM-L6-v2") #embedding model from huggingface. It's lightweight and generates 384-dimensional embeddings, suitable for tasks like clustering or semantic search

#pineclone client 
pc = Pinecone(PINECONE_API_KEY)
index_name = "youtube-transcripts-embeddings"
index = pc.Index(index_name)



#utility function create_embeddings()
def create_embedding(query):
    embedding = model.encode(query)
    return embedding.tolist()


def search_videos(top_k=5, embedding):
    try:
        result = index.query(
        vector = embedding,
        top_k = top_k,
        include_metadata = True,
        namespace = 'youtube-transcripts-embeddings'
        )
        results = []
        
        for match in result["matches"]:
            results.append({
                'id':match['id'],
                'score': match['score'],
                'url': match['metadata']['url'],
                'published_at': match['metadata']['published_at'],
                'title': match['metadata']['title']
            })  
            
        return results    
    
    except Exception as e: 
        return f"An error occurred during the search: {e}"
    


@app.route("/", methods=["GET"])
def home():  
    return {
        "data":"Whatsup Sucka!!!!"
    }
    

@app.route("/", methods=["POST"])
def search():
    data = request.get_json()
    query = data['query']
    embedding = create_embedding(query)
    result = search_videos(10, embedding)
    
    return result



if __name__ == "__main__":
    app.run(debug=True)
