# YouTube Transcript Search API

A Flask-based API that leverages Sentence Transformers and Pinecone to perform semantic searches on YouTube video transcripts. This application allows users to input a query and retrieve the most relevant YouTube videos based on the content of their transcripts.

## 📖 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoint](#api-endpoint)
  - [POST `/`](#post-search)
- [Example Usage](#example-usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Semantic Search:** Utilizes Sentence Transformers to generate embeddings for search queries.
- **Vector Database Integration:** Employs Pinecone for efficient similarity searches within a large dataset of YouTube video transcripts.
- **Scalable and Efficient:** Designed to handle multiple queries with minimal latency.
- **Secure Configuration:** Manages sensitive information like API keys using environment variables.
- **Logging and Error Handling:** Implements logging for monitoring and debugging purposes.

---

## Technologies Used

- **Backend Framework:** [Flask](https://flask.palletsprojects.com/)
- **Sentence Embeddings:** [Sentence Transformers](https://www.sbert.net/)
- **Vector Database:** [Pinecone](https://www.pinecone.io/)
- **Environment Management:** [python-dotenv](https://github.com/theskumar/python-dotenv)
- **Others:** Python 3.9+, Git

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.9+** is installed on your machine. You can download it from [here](https://www.python.org/downloads/).
- **Pinecone Account:** Sign up for a Pinecone account [here](https://www.pinecone.io/start/).
- **YouTube Data:** A dataset of YouTube video transcripts should be prepared and upserted into Pinecone under the specified namespace.

---

## Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-transcript-search-api.git
cd youtube-transcript-search-api/backend
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration

The application requires certain environment variables to function correctly. These variables store sensitive information like API keys.

### 1. Create a `.env` File

Inside the `backend/` directory, create a `.env` file:

```bash
touch .env
```

### 2. Add Environment Variables

Open the `.env` file in your preferred text editor and add the following:

```plaintext
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment  # e.g., us-east1-gcp
INDEX_NAME=youtube-transcripts-embeddings
NAMESPACE=youtube-transcripts-embeddings
FLASK_ENV=development
PORT=5000
```

**⚠️ Important:** Replace `your-pinecone-api-key` and `your-pinecone-environment` with your actual Pinecone API key and environment.

### 3. Secure Your `.env` File

Ensure that the `.env` file is not tracked by Git to protect your sensitive information.

Add `.env` to your `.gitignore`:

```gitignore
# backend/.gitignore

.env
venv/
__pycache__/
*.pyc
```

---

## Running the Application

### 1. Initialize Pinecone and Upsert Data

Before running the Flask application, ensure that your Pinecone index is set up and populated with the YouTube transcript embeddings.

**Note:** The following steps assume you have a script to upsert data into Pinecone (`dataUpsert.py`). Ensure your embeddings are correctly formatted and upserted under the specified namespace.

```bash
python3 dataUpsert.py
```

**Sample Output:**

```plaintext
Index 'youtube-transcripts-embeddings' already exists.
{'dimension': 384, 'index_fullness': 0.0, 'namespaces': {'youtube-transcripts-embeddings': {'vector_count': 143}}, 'total_vector_count': 143}
All embeddings upserted successfully.
```

### 2. Start the Flask Server

With the virtual environment activated and dependencies installed, run the Flask application:

```bash
python3 app.py
```

**Sample Output:**

```plaintext
 * Serving Flask app 'app'
 * Debug mode: on
INFO:root:Index 'youtube-transcripts-embeddings' already exists.
INFO:root:Search successful for query embedding with top_k=5
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

---

## API Endpoint

### POST `/`

#### Description

Searches for YouTube videos similar to the input query based on transcript embeddings.

#### Request

- **URL:** `/`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

  ```json
  {
      "query": "your search query here",
      "top_k": 5  # Optional, defaults to 5
  }
  ```

  - `query` (string): The search term to find similar videos.
  - `top_k` (integer, optional): Number of top similar videos to return. Defaults to 5.

#### Response

- **Success (200 OK):**

  ```json
  {
      "matches": [
          {
              "id": "qOECpFrwv-g",
              "score": 0.490659267,
              "url": "https://www.youtube.com/watch?v=tLL5FxVpibI",
              "published_at": "2024-02-02T10:35:44Z",
              "title": "Is this Real or AI Generated?"
          },
          {
              "id": "eoVPKom8iFc",
              "score": 0.424950719,
              "url": "https://www.youtube.com/watch?v=eoVPKom8iFc",
              "published_at": "2024-02-02T10:35:44Z",
              "title": "Move AI Animation for Facial and Motion Capture!"
          },
          ...
      ]
  }
  ```

  - `matches` (array): A list of similar videos.
    - `id` (string): Unique identifier of the video.
    - `score` (float): Similarity score.
    - `url` (string): URL of the YouTube video.
    - `published_at` (string): Publication date of the video in ISO format.
    - `title` (string): Title of the video.

- **Client Error (400 Bad Request):**

  ```json
  {
      "error": "Invalid request. 'query' field is required."
  }
  ```

- **Server Error (500 Internal Server Error):**

  ```json
  {
      "error": "An error occurred during the search: detailed error message"
  }
  ```

---

## Example Usage

### Using `curl`

```bash
curl -X POST http://localhost:5000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "videos about visual detection", "top_k": 5}'
```

### Using Postman or Insomnia

1. **Create a New POST Request.**
2. **Set the URL:** `http://localhost:5000/search`
3. **Set Headers:**
   - `Content-Type: application/json`
4. **Set Body:**
   ```json
   {
       "query": "videos about visual detection",
       "top_k": 5
   }
   ```
5. **Send the Request and Verify the Response.**

---

## Deployment

To deploy this Flask application to a production environment, consider the following steps:

### 1. Choose a Hosting Platform

Options include:

- [Heroku](https://www.heroku.com/)
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
- [Google App Engine](https://cloud.google.com/appengine)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform/)
- [Azure App Service](https://azure.microsoft.com/en-us/services/app-service/)

### 2. Configure Environment Variables

Ensure that all necessary environment variables are securely set on the hosting platform.

### 3. Use a Production WSGI Server

Replace the built-in Flask server with a production-ready server like Gunicorn.

**Example with Gunicorn:**

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

### 4. Secure the Application

- **Use HTTPS:** Ensure that your application is served over HTTPS.
- **Implement Authentication:** Secure your API endpoints if necessary.
- **Monitor Logs:** Set up logging and monitoring to track application health and performance.

### 5. Scale as Needed

Configure auto-scaling based on traffic to handle varying loads efficiently.

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository**
2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

- [Sentence Transformers](https://www.sbert.net/) for providing efficient sentence embedding models.
- [Pinecone](https://www.pinecone.io/) for their scalable vector database solutions.
- [Flask](https://flask.palletsprojects.com/) for being a lightweight and flexible web framework.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for easy management of environment variables.

---

## Troubleshooting

### Common Issues

1. **`NameError: name 'API_KEY' is not defined`**

   - **Cause:** Missing quotes around the environment variable name in `os.getenv()`.
   - **Solution:** Use `os.getenv("API_KEY")` instead of `os.getenv(API_KEY)`.

2. **No Matches Returned**

   - **Ensure that embeddings are correctly upserted into Pinecone under the specified namespace.**
   - **Verify that the namespace in the search query matches the upsert namespace.**
   - **Check the dimensionality of the embeddings to ensure consistency.**

3. **Pinecone Client Initialization Errors**

   - **Ensure that the Pinecone API key and environment are correctly set in the `.env` file.**
   - **Verify that the Pinecone index exists and is correctly connected.**

4. **Model Loading Delays**

   - **Initialize the SentenceTransformer model once at the start to avoid delays during each request.**

5. **CORS Issues**

   - **Ensure that Flask-CORS is correctly configured to allow requests from your frontend domain.**
   - **Adjust the CORS settings as needed for your specific use case.**

---

## Contact

For any questions or support, please contact [jabhay2012@gmail.com](jabhay2012@gmail.com).

---

**Happy Searching! 🚀**