# LangCache: Semantic Caching Service for LLMs

[![GitHub license](https://img.shields.io/github/license/redis/langcache-demo)](https://github.com/redis/langcache-demo/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/redis/langcache-demo)](https://github.com/redis/langcache-demo/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/redis/langcache-demo)](https://github.com/redis/langcache-demo/issues)

## Prerequisites
- Python 3.10
- uv ([Install Guide](https://docs.astral.sh/uv/getting-started/installation/))
- Docker CLI
- Docker Compose v2
- Get the container distribution from your account team (see below)

### Import Containers
```sh
tar xzvf langcache-all-20250714-1446.tar.gz
```
```sh
docker load -i langcache-docker-image-0.0.14.tar.gz
```
```sh
docker load -i langcache-embeddings-api-docker-image-0.0.3.tar.gz
```

## Quick Setup of this app if you want to test out LangCache

**This repository demonstrates how to integrate LangCache with your applications. While you can experiment with this demo app, the primary purpose is to showcase how to implement LangCache in your own projects. So you can go to the next section to see LangCache implementation **

1. Clone this repository

2. Run the setup script:
   ```sh
   uv sync
   ```
   ```sh
   . .venv/bin/activate
   ```
   ```sh
   uv run demo setup
   ```

3. Start the services:
   ```sh
   uv run demo start
   ```

4. Open the demo application:
   [http://localhost:5001](http://localhost:5001)

5. Stop the services:
   ```sh
   uv run demo stop
   ```

## LangCache Overview

This repository is a demonstration project I've prepared to showcase how to use **LangCache**, a production-ready, RESTful service for semantic caching of LLM (Large Language Model) responses using Redis as a vector database. The focus is on helping you implement LangCache with your preferred embedding model, not on teaching LLM application development.

LangCache enables you to:
- **Reduce LLM API costs** by caching semantically similar queries
- **Improve response times** by retrieving cached responses (milliseconds vs. seconds)
- **Choose your embedding model** (OpenAI, Ollama, Redis Langcache, or custom models)
- **Scale efficiently** with Redis vector search capabilities
- **Monitor performance** with detailed metrics and logs

> **Note:** This demo focuses on LangCache operations, deployment details, and cache configuration. The included LLM app is simply a vehicle to demonstrate the caching capabilities.

---

## Project Structure

```
langcache-operations/      # Main LangCache service (RESTful API, cache logic)
  └─ embeddings/           # Embedding API (supports OpenAI, Redis Langcache, Ollama)
llm-app/                   # Demo application to showcase LangCache capabilities
  ├─ templates/            # UI templates for the demo app
  ├─ static/               # CSS and JavaScript files
  └─ log_manager.py        # Cache log tracking and visualization
docker-compose.yaml        # Orchestrates all services
README.md
```

---

## Core components

LangCache is designed with a modular architecture that separates concerns and allows for flexible deployment options:

- **LangCache Service**: Core RESTful API that handles all cache operations, vector similarity search, and metrics
   - **Embeddings API**: Provides vector embeddings for queries with support for multiple models:
     - Redis Langcache: Uses the `redis/langcache-embed-v1` model from Hugging Face
     - OpenAI: Integrates with OpenAI's embedding models
     - Ollama: Uses local embedding models for self-hosted deployments
- **Redis**: Serves as the database that stores embeddings and cached responses, enabling fast similarity search
- **Demo Application**: (Optional) Provides a user interface to demonstrate LangCache capabilities and visualize cache performance

---

## Workflow Comparison

### Traditional LLM Application Flow (Without LangCache)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Query │────▶│  LLM API    │────▶│  Response   │
└─────────────┘     │  (OpenAI,   │     │  to User    │
                    │  Gemini,    │     └─────────────┘
                    │  etc.)      │
                    └─────────────┘
```

1. **User Query**: Application receives a query from the user
2. **LLM Processing**: Query is sent directly to the LLM API (OpenAI, Gemini, etc.)
3. **Response**: LLM generates a response and returns it to the user

**Limitations**:
- Every query requires a full LLM API call (high latency, 1-10 seconds)
- Repeated or similar questions incur the same cost and delay
- API costs accumulate with each query
- No ability to reuse previous responses

### LangCache-Enhanced LLM Application Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Query │────▶│  Embedding  │────▶│  Cache      │
└─────────────┘     │  Generation │     │  Lookup     │
                    └─────────────┘     └──────┬──────┘
                                               │
                                               ├─────────── Cache Hit ───────────┐
                                               │                                 │
                                               │                                 ▼
                                               │                          ┌─────────────┐
                                               │                          │  Response   │
                                               │                          │  to User    │
                                               │                          └─────────────┘
                                               │                                 ▲
                                               │ Cache Miss                      │
                                               ▼                                 │
                                        ┌─────────────┐                          │
                                        │  Call to    │─────────────────────────┘
                                        │  LLM        │             │
                                        └─────────────┘             │
                                                                    ▼
                                                             Cache Storage
```

#### Key Components of the LangCache Flow:

1. **Cache Initialization**:
   - Create a cache with a specific embedding model (Redis Langcache, OpenAI, Ollama)
   - Define similarity threshold (e.g., 0.85) for semantic matching
   - Set TTL (time-to-live) for cache entries if needed
   - Cache ID is returned and stored for future operations

2. **Embedding Generation**:
   - User query is converted to a vector embedding using the selected model
   - This embedding represents the semantic meaning of the query
   - The embedding service handles all model-specific operations

3. **Cache Lookup (Semantic Search)**:
   - The query embedding is compared to all stored embeddings in Redis
   - Redis performs a vector similarity search 
   - If a match above the similarity threshold is found, it's a cache hit
   - If no match is found, it's a cache miss

4. **Response Handling**:
   - **Cache Hit**: Return the cached response immediately (milliseconds)
   - **Cache Miss**: Forward the query to the LLM API, then store the response in the cache for future use

**Benefits**:
- Dramatically reduced response times for similar queries (milliseconds vs. seconds)
- Lower API costs through reuse of previous responses
- Semantic matching finds relevant responses even when queries are worded differently
- Scalable with Redis as the vector database backend

---

## LangCache Deployment Guide

LangCache full deployment guide is here : https://miniature-goggles-w6ozyrr.pages.github.io/ but if you want to know how I implemented in this project then you can read a short version here

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
- API keys for your preferred embedding model:
  - OpenAI API key for OpenAI embeddings
  - Hugging Face token for Redis Langcache embeddings
  - No API key needed for Ollama (runs locally)

### Getting Started with Docker Compose

1. **Load the LangCache Docker image:**
   ```sh
   docker load -i docker-image-langcache-<version>.tar
   ```

2. **Choose your embedding model:**
   LangCache supports multiple embedding models so you can choose what option you want to go with for your LangCache. This demo showcases three options:

   **Option 1: Redis Langcache Embedding (Default in this app )**
   ```sh
   docker-compose up -d langcache-redis embeddings
   ```
   This uses the `redis/langcache-embed-v1` model from Hugging Face, which is optimized for semantic caching and set as the default in this demo.

   **Option 2: OpenAI Embeddings**
   ```sh
   # First, set your OpenAI API key in docker-compose.yaml
   docker-compose up -d langcache-openai
   ```
   Demonstrates integration with OpenAI's text-embedding-3-small model (requires API key).

   **Option 3: Ollama Embeddings**
   ```sh
   docker-compose up -d langcache-ollama ollama
   ```
   Shows how to use Ollama's local embedding models for a fully self-hosted solution.

3. **Start the demo application (optional):**
   ```sh
   docker-compose up -d llm-app
   ```
   This starts a simple web UI to demonstrate LangCache in action.

4. **Access the services:**
   - LangCache API: [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)
   - Demo Application: [http://localhost:5001](http://localhost:5001)
   - Cache Log Dashboard: [http://localhost:5001/log](http://localhost:5001/log)

5. **Cleanup:**
   ```sh
   # Stop the services
   docker-compose down

   # Remove the Docker image
   docker image ls | grep langcache | awk '{print $3}' | xargs docker image rm
   ```

### Kubernetes Deployment

For production deployments, LangCache provides Helm charts:

1. **Prerequisites:**
   - Docker and Helm installed
   - Kubernetes enabled in Docker Desktop or a cloud provider

2. **Load the Docker image:**
   ```sh
   docker load -i docker-image-langcache-<version>.tar
   ```

3. **Set your OpenAI API key (if using OpenAI embeddings):**
   ```sh
   export OPENAI_API_KEY="<your-key-here>"
   ```

4. **Create a values file:**
   ```yaml
   # myvalues.yaml
   embeddings:
     defaultModel: redis-langcache  # or openai, ollama
     models:
       redis-langcache:
         name: redis-langcache-embed-v1
         dimensions: 384
         baseUrl: http://embeddings:8080
         apiKey: ${HF_TOKEN}
   ingress:
     enabled: true
     className: "nginx"
     hosts:
       - host: localhost
         paths:
           - path: /
             pathType: ImplementationSpecific
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
   env:
     LOGGING_LEVEL_ROOT: info
   ```

5. **Deploy with Helm:**
   ```sh
   helm install langcache -f myvalues.yaml helm-package-langcache-<version>.tgz
   ```

6. **Cleanup:**
   ```sh
   # Uninstall the service
   helm uninstall langcache

   # Remove the Docker image
   docker image ls | grep langcache | awk '{print $3}' | xargs docker image rm
   ```

---

## LangCache API Reference

LangCache exposes a RESTful API for all cache operations. The main endpoints are:

### 1. Create a Cache
```
POST /v1/admin/caches
{
  "indexName": "my-cache-index",
  "redisUrls": ["redis://localhost:6379"],
  "modelName": "redis-langcache",
  "defaultSimilarityThreshold": 0.85,
  "defaultTtlMillis": 3600000
}
```
**Response:**
```
{
  "cacheId": "my-cache-id",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 2. Search the Cache (Semantic Lookup)
```
POST /v1/caches/{cacheId}/search
{
  "prompt": "What is the capital of France?",
  "similarityThreshold": 0.85
}
```
**Response:**
```
[
  {
    "id": "myIndex:5b84acef...",
    "prompt": "What is the capital of France?",
    "response": "Paris",
    "similarity": 0.92,
    ...
  }
]
```

### 3. Add to the Cache
```
POST /v1/caches/{cacheId}/entries
{
  "prompt": "What is the capital of France?",
  "response": "Paris"
}
```
**Response:**
```
{
  "entryId": "myIndex:5b84acef...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 4. Delete Cache Entries
```
DELETE /v1/caches/{cacheId}/entries
{
  "attributes": {"language": "en"},
  "scope": {"userId": "user-123"}
}
```

### 5. Get Cache Info
```
GET /v1/admin/caches/{cacheId}/info
```
**Response:**
```
{
  "cacheId": "my-cache-id",
  "cacheStatus": "active",
  "operationMetrics": { ... },
  "cacheMetrics": { ... },
  ...
}
```

### 6. Delete a Cache
```
DELETE /v1/admin/caches/{cacheId}
```

For complete API documentation, access the Swagger UI at [http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html).

## Observability and Monitoring

### Metrics and Logs
- **Prometheus Metrics:** Available at [http://localhost:8080/actuator/prometheus](http://localhost:8080/actuator/prometheus)
- **Service Logs:**
  - Default: `INFO` level, JSON formatted
  - Full request/response: set `LOGGING_LEVEL_ORG_ZALANDO_LOGBOOK=TRACE`

### Advanced Configuration
- **Custom Redis database:**
  ```
  METADATABASE_URLS: redis://[user]:[password]@<host>:<port>
  ```
  For TLS use `rediss://` (Sentinel deployments aren't supported)

- **Increase log verbosity:**
  ```
  LOGGING_LEVEL_ROOT: DEBUG
  LOGGING_LEVEL_ORG_ZALANDO_LOGBOOK: TRACE
  ```

### Cache Performance Dashboard

As part of this demo, I've built a structured cache log dashboard that provides valuable insights into your cache performance:

- **Cache Statistics:** Track total queries, hits, misses, and hit ratio
- **Cache Creation Events:** Monitor cache IDs and creation timestamps
- **Query History:** View detailed logs of all queries with:
  - Original query text
  - Cache hit/miss status
  - Matched query (for hits) - see which cached query was semantically matched
  - Similarity score - understand how close the match was
  - Response time - compare cache vs. LLM performance

Access the dashboard at [http://localhost:5001/log](http://localhost:5001/log).

This logging system helps you:
- Identify which queries are being cached effectively
- Understand semantic matching patterns (especially useful to see which cached query matched your input)
- Optimize your cache configuration based on similarity scores
- Measure performance improvements and cache hit ratio

---

## Conclusion

This demo showcases how to implement LangCache with different embedding models to provide efficient semantic caching for LLM applications. By following this guide, you can:

1. Deploy LangCache with your preferred embedding model (Redis Langcache, OpenAI, or Ollama)
2. Integrate it with your LLM applications using the RESTful API
3. Monitor cache performance using the built-in logging system
4. Configure advanced settings for production deployments

The included demo application demonstrates these capabilities in action, with a focus on the Redis Langcache embedding model as the default option.

---

## License
MIT

## Acknowledgments
- Redis Labs for Redis LangCache
- Hugging Face for the redis/langcache-embed-v1 model
- Google for Gemini LLM API
- OpenAI for embedding API
- Ollama for local embedding models
