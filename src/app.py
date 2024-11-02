from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

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


def search_videos(embedding, top_k):
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
            
        return jsonify(results)    
    
    except Exception as e: 
        return jsonify({"error": f"An error occurred during the search: {e}"}), 500
    


@app.route("/", methods=["GET"])
def home():  
    return jsonify({"data": "Whatsup Sucka!!!!"})
    

@app.route("/", methods=["POST"])
def search():
    data = request.get_json()
    query = data['query']
    embedding = create_embedding(query)
    result = search_videos(embedding, 10)
    
    return result



if __name__ == "__main__":
    # Use environment variables for host and port, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)