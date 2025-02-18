from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from flask_cors import CORS
from transformers import pipeline
import requests
load_dotenv()

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "*"}})


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

HF_API_KEY = os.getenv("HF_API_KEY")
headers = {"Authorization": f"Bearer {HF_API_KEY}"}
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

model = SentenceTransformer("all-MiniLM-L6-v2") #embedding model from huggingface. It's lightweight and generates 384-dimensional embeddings, suitable for tasks like clustering or semantic search





#pineclone client 
pc = Pinecone(PINECONE_API_KEY)
index_name = "youtube-transcripts-embeddings"
index = pc.Index(index_name)



#utility function create_embeddings()
def create_embedding(query):
    embedding = model.encode(query)
    return embedding.tolist()


#generate response with gpt using retrived context
def generate_response(query, context):
    prompt = f"""You are angent of the podcast called Overpowered AI. Overpowered AI covers weekly updates in the field of Artificial Intelligence. It is hosted by Varun Mayya, can be called Varun (Entraprenure in AI space) and Tanmay Bhat (Comidian and investor) can be called Tanmay.  Use this information and answer:\n\n{context}\n\nQuery: {query}\nAnswer:"""
   
    payload = {"inputs": prompt, "parameters": {"max_length": 150}}
    
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        full_text = response.json()[0]["generated_text"]
        answer = full_text.split("\nAnswer:", 1)[-1].strip()
        return answer
    else:
        return f"Error: {response.status_code}, {response.text}"


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
                'title': match['metadata']['title'],
                
            })  
            
        
        return results    
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
    matches = search_videos(embedding, 10)
    
    # Extract text from retrieved matches
    context = " ".join([match['title'] for match in matches])

    # Generate a response using GPT
    answer = generate_response(query, context)
    return jsonify({"answer": answer, "sources": matches})

    



if __name__ == "__main__":
    # Use environment variables for host and port, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)