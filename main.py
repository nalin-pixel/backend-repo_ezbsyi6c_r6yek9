import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Contactmessage, Project

app = FastAPI(title="Adley Kinsman Personal Brand API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# Schema endpoint so tooling can read Pydantic models
@app.get("/schema")
def get_schema_file():
    try:
        with open("schemas.py", "r", encoding="utf-8") as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact message submission
@app.post("/api/contact")
def submit_contact(payload: Contactmessage):
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Projects list and creation
@app.get("/api/projects", response_model=List[Project])
def list_projects(tag: Optional[str] = None, limit: Optional[int] = 20):
    try:
        filter_dict = {"tags": {"$in": [tag]}} if tag else {}
        docs = get_documents("project", filter_dict=filter_dict, limit=limit)
        # Convert ObjectId and ensure required fields
        result: List[Project] = []
        for d in docs:
            # Remove MongoDB-specific fields not in schema
            d.pop("_id", None)
            # Coerce to Project (will validate)
            result.append(Project(**d))
        return result
    except Exception as e:
        # If DB not available, return empty list gracefully
        return []

@app.post("/api/projects")
def add_project(payload: Project):
    try:
        inserted_id = create_document("project", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
