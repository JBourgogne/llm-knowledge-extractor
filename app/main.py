from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import json

# Import our local modules
from app.models import Base, Analysis
from app.llm_service import LLMService
from app.text_processor import extract_keywords

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="LLM Knowledge Extractor")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./analyses.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize LLM service
llm_service = LLMService(api_key=os.getenv("OPENAI_API_KEY"))

# Pydantic models for request/response
class TextInput(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    id: int
    summary: str
    metadata: Dict[str, Any]  # Keep this as 'metadata' for API response

# Database session manager
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/")
def read_root():
    return {"status": "healthy", "service": "LLM Knowledge Extractor"}

# Main analysis endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(input: TextInput):
    # Validate input - handle empty input edge case
    if not input.text or not input.text.strip():
        raise HTTPException(status_code=400, detail="Empty input not allowed")
    
    try:
        # Get LLM analysis
        llm_result = llm_service.analyze_text(input.text)
        
        # Extract keywords locally
        keywords = extract_keywords(input.text)
        
        # Combine results
        metadata = {
            **llm_result,
            "keywords": keywords
        }
        
        # Store in database
        with get_db() as db:
            analysis = Analysis(
                original_text=input.text[:1000],  # Truncate for storage
                summary=llm_result.get("summary", "No summary available"),
                extracted_data=metadata  # Use extracted_data for database column
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            return {
                "id": analysis.id,
                "summary": analysis.summary,
                "metadata": metadata  # Return as 'metadata' in API response
            }
        
    except HTTPException:
        raise
    except Exception as e:
        # Handle LLM API failure edge case
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Search endpoint
@app.get("/search")
async def search_analyses(topic: Optional[str] = None):
    with get_db() as db:
        query = db.query(Analysis)
        
        if topic:
            # Search in extracted_data JSON
            results = []
            for analysis in query.all():
                # Check if topic appears in extracted data
                data_str = json.dumps(analysis.extracted_data).lower() if analysis.extracted_data else ""
                if topic.lower() in data_str:
                    results.append({
                        "id": analysis.id,
                        "summary": analysis.summary,
                        "metadata": analysis.extracted_data,  # Return as 'metadata' in API
                        "created_at": analysis.created_at.isoformat() if analysis.created_at else None
                    })
            return results
        else:
            # Return all analyses
            return [
                {
                    "id": a.id,
                    "summary": a.summary,
                    "metadata": a.extracted_data,  # Return as 'metadata' in API
                    "created_at": a.created_at.isoformat() if a.created_at else None
                }
                for a in query.all()
            ]

# Optional: Batch processing endpoint
@app.post("/analyze_batch")
async def analyze_batch(inputs: List[TextInput]):
    results = []
    errors = []
    
    for idx, input_item in enumerate(inputs):
        try:
            # Reuse the analyze logic
            if not input_item.text or not input_item.text.strip():
                errors.append({"index": idx, "error": "Empty input"})
                continue
                
            llm_result = llm_service.analyze_text(input_item.text)
            keywords = extract_keywords(input_item.text)
            
            metadata = {
                **llm_result,
                "keywords": keywords
            }
            
            with get_db() as db:
                analysis = Analysis(
                    original_text=input_item.text[:1000],
                    summary=llm_result.get("summary", "No summary available"),
                    extracted_data=metadata  # Use extracted_data for database
                )
                db.add(analysis)
                db.commit()
                db.refresh(analysis)
                
                results.append({
                    "id": analysis.id,
                    "summary": analysis.summary,
                    "metadata": metadata  # Return as 'metadata' in API
                })
                
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})
    
    return {
        "successful": results,
        "errors": errors,
        "total_processed": len(results),
        "total_errors": len(errors)
    }

# Get all analyses endpoint
@app.get("/analyses")
async def get_all_analyses(limit: int = 10, offset: int = 0):
    with get_db() as db:
        analyses = db.query(Analysis).offset(offset).limit(limit).all()
        return [
            {
                "id": a.id,
                "summary": a.summary,
                "metadata": a.extracted_data,  # Return as 'metadata' in API
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in analyses
        ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)