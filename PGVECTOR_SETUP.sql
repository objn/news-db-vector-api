"""
PostgreSQL Vector Search Setup and Usage Guide

## 1. Enable pgvector extension in PostgreSQL

Connect to your database and run:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 2. Alter the news table to use vector type

Option A: If you want to keep existing data (convert from text to vector):
```sql
-- First, create a new column with vector type
ALTER TABLE news ADD COLUMN embedding_vector vector(768);

-- If you have existing embeddings as JSON strings, convert them:
UPDATE news 
SET embedding_vector = embedding::vector 
WHERE embedding IS NOT NULL;

-- Optional: Drop old column and rename new one
ALTER TABLE news DROP COLUMN embedding;
ALTER TABLE news RENAME COLUMN embedding_vector TO embedding;
```

Option B: Fresh start (if table is empty or you can recreate):
```sql
ALTER TABLE news ALTER COLUMN embedding TYPE vector(768) USING embedding::vector;
```

## 3. Create index for faster similarity search

```sql
-- Create HNSW index for cosine similarity (recommended for large datasets)
CREATE INDEX ON news USING hnsw (embedding vector_cosine_ops);

-- OR use IVFFlat index (alternative)
CREATE INDEX ON news USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

## 4. Query examples using PostgreSQL vector operations

### Find top 5 most similar news (using cosine similarity):
```sql
SELECT 
    news_id,
    news_header,
    news_desc,
    1 - (embedding <=> '[0.1, 0.2, ...]'::vector) as similarity_score
FROM news
WHERE embedding IS NOT NULL 
  AND deleted_at IS NULL
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 5;
```

### With threshold filter (only similarity >= 0.7):
```sql
SELECT 
    news_id,
    news_header,
    news_desc,
    1 - (embedding <=> '[0.1, 0.2, ...]'::vector) as similarity_score
FROM news
WHERE embedding IS NOT NULL 
  AND deleted_at IS NULL
  AND (1 - (embedding <=> '[0.1, 0.2, ...]'::vector)) >= 0.7
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

## Vector operators in PostgreSQL:

- `<->` : L2 distance (Euclidean distance)
- `<=>` : Cosine distance (1 - cosine similarity)
- `<#>` : Inner product (negative dot product)

## Performance tips:

1. Always create an index on the vector column
2. Use `LIMIT` to restrict results
3. HNSW index is faster for queries but slower for inserts
4. IVFFlat is balanced between query and insert speed

## Example: Insert news with embedding:
```sql
INSERT INTO news (news_id, news_desc, embedding)
VALUES ('news-001', 'Some news content', '[0.1, 0.2, 0.3, ...]'::vector);
```

## Example: Update existing news with embedding:
```sql
UPDATE news 
SET embedding = '[0.1, 0.2, 0.3, ...]'::vector
WHERE news_id = 'news-001';
```
"""

# This file contains SQL documentation only
# Run the SQL commands directly in your PostgreSQL database
