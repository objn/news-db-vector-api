# News Database Vector API Specification

## Overview
REST API for managing news embeddings and performing semantic similarity searches using Google AI Studio (Gemini) text-embedding-004 model.

**Base URL:** `http://localhost:9099`  
**Version:** 1.0  
**Last Updated:** October 24, 2025

---

## Table of Contents
1. [Authentication](#authentication)
2. [Health & Configuration Endpoints](#health--configuration-endpoints)
3. [Embedding Generation Endpoints](#embedding-generation-endpoints)
4. [Similarity Search Endpoints](#similarity-search-endpoints)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)

---

## Authentication
Currently, no authentication is required. (Production deployments should implement proper authentication)

---

## Health & Configuration Endpoints

### 1. Root Endpoint
```http
GET /
```

**Description:** API welcome message

**Response:**
```json
{
  "message": "Welcome to PyCosineSim API"
}
```

---

### 2. Health Check
```http
GET /health
```

**Description:** Check API service status

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

---

### 3. Configuration Info
```http
GET /config
```

**Description:** Get current configuration (sanitized)

**Response:**
```json
{
  "environment": "development",
  "database_configured": true
}
```

---

### 4. Database Connection Test
```http
GET /db/test
```

**Description:** Test database connectivity

**Response:**
```json
{
  "status": "success",
  "message": "Database connection is working"
}
```

---

## Embedding Generation Endpoints

### 1. Generate Embedding from Text
```http
POST /news-embedding
```

**Description:** Generate embedding vector from provided text

**Request Body:**
```json
{
  "news_desc": "ไฟไหม้ route66 ร้านดัง ย่านอาร์ซีเอ"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "news_desc": "ไฟไหม้ route66 ร้านดัง ย่านอาร์ซีเอ",
    "embedding": [0.123, -0.456, 0.789, ...],
    "embedding_dimension": 768,
    "model": "text-embedding-004"
  }
}
```

**Parameters:**
- `news_desc` (string, required): Text to generate embedding from

---

### 2. Generate & Save Embedding by News ID
```http
POST /news-embedding-id/
```

**Description:** Fetch news from database by ID, generate embedding from news_desc, and save to database

**Request Body:**
```json
{
  "news_id": "bab83845-3d38-41a2-8d03-3a3994c5ca0c"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Embedding created and saved successfully",
  "data": {
    "news_id": "bab83845-3d38-41a2-8d03-3a3994c5ca0c",
    "news_header": "ไฟไหม้ที่เก็บอุปกรณ์ ร้าน Route66",
    "news_desc": "ไฟไหม้ route66 ร้านดัง ย่านอาร์ซีเอ...",
    "embedding_dimension": 768,
    "date_time": "2025-10-06 17:17:00",
    "model": "text-embedding-004"
  }
}
```

**Parameters:**
- `news_id` (string, required): Unique identifier of news item

**Error Responses:**
- `404`: News item not found
- `400`: News description is empty

---

### 3. Batch Generate Embeddings for All News
```http
POST /news-embedding/batch/all
```

**Description:** Generate embeddings for all news items that don't have embeddings yet

**Request Body:** None (empty)

**Response:**
```json
{
  "status": "success",
  "message": "Processed 150 news items",
  "data": {
    "processed": 150,
    "success": 145,
    "failed": 5,
    "failed_items": [
      {
        "news_id": "news-999",
        "reason": "Empty news_desc"
      }
    ]
  }
}
```

**Notes:**
- Only processes news where `embedding IS NULL`
- Skips deleted news (`deleted_at IS NOT NULL`)
- Returns top 10 failed items if any failures occur

---

## Similarity Search Endpoints

### 1. Find Similar News
```http
POST /news-similarity-compare
```

**Description:** Compare input text/embedding with all news in database and return most similar items

**Request Body (Option 1 - Text):**
```json
{
  "news_desc": "ไฟไหม้ ร้านอาหาร กรุงเทพ",
  "threshold": 0.7,
  "top_k": 5
}
```

**Request Body (Option 2 - Pre-computed Embedding):**
```json
{
  "news_desc": "ไฟไหม้ ร้านอาหาร กรุงเทพ",
  "embedding": "[0.123, -0.456, 0.789, ...]",
  "threshold": 0.7,
  "top_k": 5
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "query": "ไฟไหม้ ร้านอาหาร กรุงเทพ",
    "results": [
      {
        "news_id": "bab83845-3d38-41a2-8d03-3a3994c5ca0c",
        "news_header": "ไฟไหม้ที่เก็บอุปกรณ์ ร้าน Route66",
        "news_desc": "ไฟไหม้ route66 ร้านดัง ย่านอาร์ซีเอ...",
        "similarity_score": 0.8934,
        "date_time": "2025-10-06 17:17:00"
      },
      {
        "news_id": "abc12345-6789-0123-4567-890abcdef012",
        "news_header": "เพลิงไหม้ร้านค้า ในกรุงเทพ",
        "news_desc": "เกิดเพลิงไหม้ร้านค้าในย่านธุรกิจ...",
        "similarity_score": 0.8521,
        "date_time": "2025-10-05 14:30:00"
      }
    ],
    "total_compared": 1000,
    "total_above_threshold": 25,
    "top_k": 5,
    "threshold": 0.7,
    "method": "python_cosine_similarity"
  }
}
```

**Parameters:**
- `news_desc` (string, required): Text to compare
- `embedding` (string, optional): Pre-computed embedding as JSON array string
- `threshold` (float, optional, default: 0.7): Minimum similarity score (0.0 - 1.0)
- `top_k` (integer, optional, default: 1): Number of top results to return

**Similarity Score:**
- Range: 0.0 to 1.0
- 1.0 = Identical meaning
- 0.0 = Completely different
- Typical threshold: 0.7-0.8

**Notes:**
- If `embedding` is provided, it will be used directly
- If `embedding` is not provided, will generate from `news_desc`
- Results are sorted by similarity score (descending)

---

## Data Models

### NewsEmbeddingRequest
```typescript
{
  news_desc: string  // Required
}
```

### NewsEmbeddingRequest_ID
```typescript
{
  news_id: string  // Required
}
```

### EmbeddingCompareRequest
```typescript
{
  news_desc: string           // Required
  embedding?: string | null   // Optional - JSON array as string
  threshold?: number          // Optional - Default: 0.7
  top_k?: number             // Optional - Default: 1
}
```

### News (Database Model)
```typescript
{
  news_id: string             // Primary key
  news_header: string         // Headline
  news_desc: string           // Description
  news_source: string         // Source
  date_time: string           // Publication date/time
  keyword_location: string    // Location keywords
  hashtag: string             // Hashtags
  news_type_id: string        // Type identifier
  embedding: string           // JSON array of floats (768-dim)
  created_at: datetime
  updated_at: datetime
  deleted_at: datetime | null // Soft delete
}
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters or empty data |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server-side error |

### Common Error Scenarios

**400 Bad Request:**
```json
{
  "detail": "Invalid embedding format. Must be JSON array."
}
```

**404 Not Found:**
```json
{
  "detail": "News item with ID 'xyz' not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error generating embedding: Connection timeout"
}
```

---

## Technical Details

### Embedding Model
- **Model:** Google AI Studio `text-embedding-004`
- **Dimension:** 768
- **Task Type:** `SEMANTIC_SIMILARITY`
- **Optimal for:** Text comparison and similarity search

### Similarity Calculation
- **Method:** Cosine Similarity
- **Formula:** `score = (A · B) / (||A|| × ||B||)`
- **Range:** [-1, 1] normalized to [0, 1]

### Performance Considerations
- **Batch Processing:** Use `/news-embedding/batch/all` for bulk operations
- **Caching:** Pre-compute embeddings for frequently accessed news
- **Indexing:** Consider implementing PostgreSQL pgvector for faster queries (see PGVECTOR_SETUP.sql)

---

## Example Usage Scenarios

### Scenario 1: Real-time Similarity Search
```bash
# Step 1: Generate embedding for query
curl -X POST http://localhost:9099/news-similarity-compare \
  -H "Content-Type: application/json" \
  -d '{
    "news_desc": "เกิดอุบัติเหตุรถชนบนถนนสุขุมวิท",
    "threshold": 0.75,
    "top_k": 10
  }'
```

### Scenario 2: Batch Processing New News
```bash
# Step 1: Save new news to database (outside API)
# Step 2: Generate embeddings for all new items
curl -X POST http://localhost:9099/news-embedding/batch/all
```

### Scenario 3: Update Single News Embedding
```bash
# After editing news content
curl -X POST http://localhost:9099/news-embedding-id/ \
  -H "Content-Type: application/json" \
  -d '{
    "news_id": "bab83845-3d38-41a2-8d03-3a3994c5ca0c"
  }'
```

---

## Environment Configuration

Required environment variables (`.env`):
```env
DATABASE_URL=postgresql://user:password@host:port/database
NODE_ENV=development
app_port=9099
GEMINI_API_KEY=your_google_ai_studio_api_key
```

---

## Database Schema

### Table: news
```sql
CREATE TABLE news (
    news_id VARCHAR(255) PRIMARY KEY,
    news_header TEXT,
    news_desc TEXT,
    news_source TEXT,
    date_time VARCHAR(255),
    keyword_location VARCHAR(255),
    hashtag VARCHAR(255),
    news_type_id VARCHAR(255),
    embedding TEXT,  -- JSON array as string
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);
```

---

## Rate Limits
- Google AI Studio API: Check your quota limits
- Database connections: Pool size = 5, Max overflow = 10

---

## Future Improvements
1. Implement authentication & authorization
2. Add pagination for batch operations
3. Implement caching layer (Redis)
4. Add PostgreSQL pgvector support for faster queries
5. Implement async processing for batch operations
6. Add API versioning
7. Implement request rate limiting

---

## Support & Documentation
- **GitHub:** [Repository URL]
- **Issues:** [Issues URL]
- **Contact:** [Contact Email]

---

**Generated:** October 24, 2025  
**API Version:** 1.0  
**Framework:** FastAPI  
**Python Version:** 3.11+
