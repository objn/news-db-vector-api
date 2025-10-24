from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from config import settings
from database import get_db, test_connection
from request_class import HealthResponse, NewsEmbeddingRequest, NewsEmbeddingRequest_ID, EmbeddingCompareRequest
from embedding_service import generate_embedding, cosine_similarity
from models import News
import json

app = FastAPI(title="NEWS-DB-VECTOR-API", redirect_slashes=False)

# Test database connection on startup
@app.on_event("startup")
async def startup_event():
    print("\n🚀 Starting up...")
    print("\n Startup api path:", settings.STARTUP_API_PATH)
    test_connection()

@app.get(f"{settings.STARTUP_API_PATH}/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to NEWS-DB-VECTOR-API"}


@app.get(f"/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", message="Service is running")


@app.get(f"{settings.STARTUP_API_PATH}/config")
async def get_config():
    """Get current configuration (sanitized)"""
    return {
        "environment": settings.NODE_ENV,
        "database_configured": bool(settings.DATABASE_URL)
    }


@app.get(f"{settings.STARTUP_API_PATH}/db/test")
async def test_db_connection():
    """Test database connection"""
    try:
        result = test_connection()
        return {
            "status": "success" if result else "failed",
            "message": "Database connection is working" if result else "Database connection failed"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post(f"{settings.STARTUP_API_PATH}/embedding")
async def create_news_embedding(request: NewsEmbeddingRequest):
    """Create a news embedding using Google AI Studio"""
    try:
        # Generate embedding using Google's text-embedding-004 model
        embedding = generate_embedding(
            text=request.news_desc,
            task_type="SEMANTIC_SIMILARITY"  # เหมาะสำหรับการค้นหาความคล้าย
        )
        
        return {
            "status": "success",
            "data": {
                "news_desc": request.news_desc,
                "embedding": embedding,
                "embedding_dimension": len(embedding),
                "model": "text-embedding-004"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")

@app.post(f"{settings.STARTUP_API_PATH}/embedding-id")
async def create_news_embedding_by_id(request: NewsEmbeddingRequest_ID, db: Session = Depends(get_db)):
    """Search news by ID, generate embedding from news_desc, and save to database"""
    try:
        # ค้นหาข่าวจาก news_id
        news_item = db.query(News).filter(News.news_id == request.news_id, News.deleted_at.is_(None)).first()

        if not news_item:
            raise HTTPException(status_code=404, detail=f"News item with ID '{request.news_id}' not found")

        if not news_item.news_desc:
            raise HTTPException(status_code=400, detail="News description is empty, cannot generate embedding")
        
        # แปลง news_desc เป็น string และจัดการ encoding อย่างระมัดระวัง
        try:
            if isinstance(news_item.news_desc, bytes):
                # ถ้าเป็น bytes ให้ decode เป็น UTF-8
                news_text = news_item.news_desc.decode('utf-8', errors='replace')
            elif isinstance(news_item.news_desc, str):
                # ถ้าเป็น string แล้ว ใช้ตรงๆ
                news_text = news_item.news_desc
            else:
                # ถ้าเป็นประเภทอื่น ให้แปลงเป็น string
                news_text = str(news_item.news_desc)
            
            # ตรวจสอบว่าไม่ใช่ string ว่าง
            if not news_text or news_text.strip() == "":
                raise HTTPException(status_code=400, detail="News description is empty after decoding")
                
        except Exception as decode_error:
            raise HTTPException(status_code=400, detail=f"Error decoding news description: {str(decode_error)}")
        
        # Generate embedding จาก news_desc
        embedding = generate_embedding(
            text=news_text,
            task_type="SEMANTIC_SIMILARITY"  # เหมาะสำหรับการค้นหาความคล้าย
        )
        
        # แปลง embedding เป็น JSON string เพื่อบันทึกในฐานข้อมูล
        embedding_json = json.dumps(embedding, ensure_ascii=False)
        
        # บันทึก embedding กลับเข้า database
        news_item.embedding = embedding_json
        db.commit()
        db.refresh(news_item)
        
        return {
            "status": "success",
            "message": "Embedding created and saved successfully",
            "data": {
                "news_id": news_item.news_id,
                "news_header": str(news_item.news_header) if news_item.news_header else "",
                "news_desc": news_text[:200] + "..." if len(news_text) > 200 else news_text,
                "embedding_dimension": len(embedding),
                "date_time": str(news_item.date_time) if news_item.date_time else None,
                "model": "text-embedding-004"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error creating news embedding: {str(e)}")


@app.post(f"{settings.STARTUP_API_PATH}/embedding/batch/all")
async def create_embeddings_for_all_news(db: Session = Depends(get_db)):
    """Generate embeddings for all news that don't have embeddings yet"""
    try:
        # ค้นหาข่าวทั้งหมดที่ยังไม่มี embedding
        news_without_embeddings = db.query(News).filter(
            News.embedding.is_(None),
            News.deleted_at.is_(None),
            News.news_desc.isnot(None)
        ).all()
        
        if not news_without_embeddings:
            return {
                "status": "success",
                "message": "All news already have embeddings",
                "data": {
                    "processed": 0,
                    "success": 0,
                    "failed": 0
                }
            }
        
        success_count = 0
        failed_count = 0
        failed_items = []
        
        for news_item in news_without_embeddings:
            try:
                if news_item.news_desc and news_item.news_desc.strip() != "":
                    # แปลงเป็น string และจัดการ encoding
                    news_text = str(news_item.news_desc)
                    if isinstance(news_item.news_desc, bytes):
                        news_text = news_item.news_desc.decode('utf-8', errors='ignore')
                    
                    # Generate embedding
                    embedding = generate_embedding(
                        text=news_text,
                        task_type="SEMANTIC_SIMILARITY"  # เหมาะสำหรับการค้นหาความคล้าย
                    )
                    
                    # บันทึก embedding (ensure_ascii=False สำหรับภาษาไทย)
                    news_item.embedding = json.dumps(embedding, ensure_ascii=False)
                    success_count += 1
                else:
                    failed_count += 1
                    failed_items.append({
                        "news_id": news_item.news_id,
                        "reason": "Empty news_desc"
                    })
            except Exception as e:
                failed_count += 1
                failed_items.append({
                    "news_id": news_item.news_id,
                    "reason": str(e)
                })
        
        # Commit ทั้งหมด
        db.commit()
        
        return {
            "status": "success",
            "message": f"Processed {len(news_without_embeddings)} news items",
            "data": {
                "processed": len(news_without_embeddings),
                "success": success_count,
                "failed": failed_count,
                "failed_items": failed_items[:10] if failed_items else []  # แสดงแค่ 10 รายการแรก
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error batch creating embeddings: {str(e)}")

@app.post(f"{settings.STARTUP_API_PATH}/similarity-compare")
async def compare_embeddings(request: EmbeddingCompareRequest, db: Session = Depends(get_db)):
    """Compare embeddings for similarity with news in database using PostgreSQL vector operations"""
    try:
        # ถ้ามี embedding ส่งมา ให้ใช้ embedding นั้น ถ้าไม่มีให้ generate จาก news_desc
        if request.embedding is not None and request.embedding.strip() != "":
            # ใช้ embedding ที่ส่งมา (parse จาก JSON string)
            try:
                query_embedding = json.loads(request.embedding)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid embedding format. Must be JSON array.")
        else:
            # Generate embedding จาก news_desc (ใช้ SEMANTIC_SIMILARITY สำหรับการค้นหา)
            query_embedding = generate_embedding(
                text=request.news_desc,
                task_type="SEMANTIC_SIMILARITY"  # เหมาะสำหรับการเปรียบเทียบความคล้าย
            )
        
        # แปลง embedding เป็น JSON string สำหรับ PostgreSQL
        embedding_json = json.dumps(query_embedding)
        
        # ใช้ Python loop เพราะ PostgreSQL vector extension อาจยังไม่ได้ติดตั้ง
        # ดึงข้อมูลข่าวทั้งหมดที่มี embedding จาก database
        all_news = db.query(News).filter(News.embedding.isnot(None)).filter(News.deleted_at.is_(None)).all()
        
        if not all_news:
            return {
                "status": "success",
                "message": "ไม่พบข่าวที่มี embedding ในฐานข้อมูล",
                "data": {
                    "query": request.news_desc,
                    "results": [],
                    "total_compared": 0
                }
            }
        
        # คำนวณ similarity score กับข่าวทั้งหมด
        similarities = []
        for news in all_news:
            if news.embedding:
                try:
                    # Parse embedding จาก string เป็น list
                    news_embedding = json.loads(news.embedding)
                    
                    # คำนวณ cosine similarity
                    score = cosine_similarity(query_embedding, news_embedding)
                    
                    # Debug: ถ้าข้อความเหมือนกันแต่ score ไม่ใช่ 1.0
                    is_exact_match = news.news_desc == request.news_desc if news.news_desc else False
                    
                    # กรองตาม threshold
                    if score >= request.threshold:
                        result_item = {
                            "news_id": news.news_id,
                            "news_header": news.news_header,
                            "news_desc": news.news_desc[:200] + "..." if news.news_desc and len(news.news_desc) > 200 else news.news_desc,
                            "similarity_score": round(score, 4),
                            "date_time": str(news.date_time) if news.date_time else None
                        }
                        
                        # เพิ่ม debug info ถ้าข้อความเหมือนกันแต่ score ไม่ใช่ 1.0
                        if is_exact_match and score < 0.99:
                            result_item["debug_warning"] = "Text matches but similarity < 0.99. Embedding may have been generated from different text."
                        
                        similarities.append(result_item)
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    # ถ้า parse embedding ไม่ได้ ให้ข้ามไป
                    continue
        
        # เรียงจากมากไปน้อย และเลือก top_k
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_results = similarities[:request.top_k]
        
        return {
            "status": "success",
            "data": {
                "query": request.news_desc,
                "results": top_results,
                "total_compared": len(all_news),
                "total_above_threshold": len(similarities),
                "top_k": request.top_k,
                "threshold": request.threshold,
                "method": "python_cosine_similarity"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing embeddings: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")
