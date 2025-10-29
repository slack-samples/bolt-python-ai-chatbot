from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, QueryConversion, Guidance, MessageResponse, Standardization, Tag

from pydantic import BaseModel
import datetime

Base.metadata.create_all(bind=engine)
app = FastAPI()

# --- Schemas ---
class QueryConversionSchema(BaseModel):
    id: Optional[int]
    asset_title: str
    type: str
    source_format: str
    target_format: str
    source_query: str
    target_query: str
    customer_name: str
    explanation: Optional[str]
    added_by: Optional[str]
    added_on: Optional[datetime.datetime]

class GuidanceSchema(BaseModel):
    id: Optional[int]
    title: str
    source_format: str
    target_format: str
    customer_name: str
    description: str
    last_updated: Optional[datetime.datetime]
    updated_by: Optional[str]

class MessageResponseSchema(BaseModel):
    id: Optional[int]
    issue_topic: str
    message: str
    customer_name: str
    responder: Optional[str]
    responder_role: str
    channel: Optional[str]
    timestamp: Optional[datetime.datetime]
    tags: Optional[str]

class StandardizationSchema(BaseModel):
    id: Optional[int]
    item: str
    details: Optional[str]
    status: Optional[str] = "draft"
    last_updated: Optional[datetime.datetime]
    updated_by: Optional[str]
    related_guidance_id: Optional[int]

class TagSchema(BaseModel):
    id: Optional[int]
    label: str

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Query Conversion Endpoints ---
@app.post('/conversions/', response_model=QueryConversionSchema)
def create_query_conversion(conv: QueryConversionSchema, db: Session = next(get_db())):
    db_obj = QueryConversion(**conv.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get('/conversions/', response_model=List[QueryConversionSchema])
def list_query_conversions(customer_name: Optional[str] = None, db: Session = next(get_db())):
    q = db.query(QueryConversion)
    if customer_name:
        q = q.filter(QueryConversion.customer_name == customer_name)
    return q.all()

@app.get('/conversions/search/', response_model=List[QueryConversionSchema])
def search_conversions(query: str = Query(...), db: Session = next(get_db())):
    # Simple text search for asset_title or explanation
    q = db.query(QueryConversion).filter(
        (QueryConversion.asset_title.contains(query)) | (QueryConversion.explanation.contains(query))
    )
    return q.all()

# --- Guidance Endpoints ---
@app.post('/guidance/', response_model=GuidanceSchema)
def create_guidance(item: GuidanceSchema, db: Session = next(get_db())):
    db_obj = Guidance(**item.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get('/guidance/', response_model=List[GuidanceSchema])
def list_guidance(customer_name: Optional[str] = None, db: Session = next(get_db())):
    q = db.query(Guidance)
    if customer_name:
        q = q.filter(Guidance.customer_name == customer_name)
    return q.all()

@app.get('/guidance/search/', response_model=List[GuidanceSchema])
def search_guidance(title: str = Query(...), db: Session = next(get_db())):
    q = db.query(Guidance).filter(Guidance.title.contains(title))
    return q.all()

# --- Message Response Endpoints ---
@app.post('/responses/', response_model=MessageResponseSchema)
def create_message_response(item: MessageResponseSchema, db: Session = next(get_db())):
    db_obj = MessageResponse(**item.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get('/responses/', response_model=List[MessageResponseSchema])
def list_message_responses(issue_topic: Optional[str] = None, customer_name: Optional[str] = None, db: Session = next(get_db())):
    q = db.query(MessageResponse)
    if issue_topic:
        q = q.filter(MessageResponse.issue_topic == issue_topic)
    if customer_name:
        q = q.filter(MessageResponse.customer_name == customer_name)
    return q.all()

@app.get('/responses/search/', response_model=List[MessageResponseSchema])
def search_responses(tag: Optional[str] = None, db: Session = next(get_db())):
    q = db.query(MessageResponse)
    if tag:
        q = q.filter(MessageResponse.tags.contains(tag))
    return q.all()

# --- Standardization Endpoints ---
@app.post('/standardizations/', response_model=StandardizationSchema)
def create_standardization(item: StandardizationSchema, db: Session = next(get_db())):
    db_obj = Standardization(**item.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get('/standardizations/', response_model=List[StandardizationSchema])
def list_standardizations(status: Optional[str] = None, db: Session = next(get_db())):
    q = db.query(Standardization)
    if status:
        q = q.filter(Standardization.status == status)
    return q.all()

@app.get('/standardizations/search/', response_model=List[StandardizationSchema])
def search_standardizations(query: str = Query(...), db: Session = next(get_db())):
    q = db.query(Standardization).filter(Standardization.item.contains(query))
    return q.all()

# --- Tag Endpoints ---
@app.post('/tags/', response_model=TagSchema)
def create_tag(tag: TagSchema, db: Session = next(get_db())):
    db_obj = Tag(**tag.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get('/tags/', response_model=List[TagSchema])
def list_tags(db: Session = next(get_db())):
    return db.query(Tag).all()


# COMPLEX QUERIES
def parse_args(args_str: str) -> Dict:
    parts = args_str.strip().split()
    if not parts:
        raise ValueError("No arguments provided.")
    obj_type = parts[0].lower()
    fields = {}
    for item in parts[1:]:
        if '=' in item:
            key, value = item.split('=', 1)
            fields[key] = value.strip('"')
    return obj_type, fields


@app.post("/init_bot/")
def init_bot(args: Dict[str, str] = Body(...), db: Session = next(SessionLocal())):
    args_str = args.get("args_str", "")
    obj_type, fields = parse_args(args_str)

    if obj_type == "conversion":
        required = {"asset_title", "type", "source_format", "target_format", "source_query", "target_query",
                    "customer_name"}
        if not required.issubset(fields):
            raise HTTPException(status_code=400, detail=f"Missing fields for conversion: {required - set(fields)}")
        obj = QueryConversion(**fields)
        db.add(obj)
    elif obj_type == "guidance":
        required = {"title", "source_format", "target_format", "customer_name", "description"}
        if not required.issubset(fields):
            raise HTTPException(status_code=400, detail=f"Missing fields for guidance: {required - set(fields)}")
        obj = Guidance(**fields)
        db.add(obj)
    elif obj_type == "response":
        required = {"issue_topic", "message", "customer_name", "responder_role"}
        if not required.issubset(fields):
            raise HTTPException(status_code=400, detail=f"Missing fields for response: {required - set(fields)}")
        obj = MessageResponse(**fields)
        db.add(obj)
    elif obj_type == "standardization":
        required = {"item"}
        if not required.issubset(fields):
            raise HTTPException(status_code=400, detail=f"Missing fields for standardization: {required - set(fields)}")
        obj = Standardization(**fields)
        db.add(obj)
    elif obj_type == "tag":
        required = {"label"}
        if not required.issubset(fields):
            raise HTTPException(status_code=400, detail=f"Missing fields for tag: {required - set(fields)}")
        obj = Tag(**fields)
        db.add(obj)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown object type: {obj_type}")

    db.commit()
    db.refresh(obj)
    return {"status": "success", "type": obj_type, "id": obj.id, "data": fields}

@app.get('/conversions/specific/', response_model=List[QueryConversionSchema])
def get_specific_conversion(
    id: Optional[int] = None,
    asset_title: Optional[str] = None,
    type: Optional[str] = None,
    source_format: Optional[str] = None,
    target_format: Optional[str] = None,
    customer_name: Optional[str] = None,
    explanation: Optional[str] = None,
    db: Session = next(SessionLocal())
):
    q = db.query(QueryConversion)
    if id:
        q = q.filter(QueryConversion.id == id)
    if asset_title:
        q = q.filter(QueryConversion.asset_title.ilike(f"%{asset_title}%"))
    if type:
        q = q.filter(QueryConversion.type == type)
    if source_format:
        q = q.filter(QueryConversion.source_format == source_format)
    if target_format:
        q = q.filter(QueryConversion.target_format == target_format)
    if customer_name:
        q = q.filter(QueryConversion.customer_name == customer_name)
    if explanation:
        q = q.filter(QueryConversion.explanation.ilike(f"%{explanation}%"))
    results = q.all()
    if not results:
        raise HTTPException(status_code=404, detail="No matching conversions found.")
    return results
# --- Slackbot Compatibility ---
# These endpoints are ready for Slackbot webhooks, app mention handlers, and slash commands!
# For example, you can configure the bot to POST when a conversion is mentioned,
# GET/search for guidance when a question arises, or fetch standardizations by status for review.

# Add PATCH/PUT/DELETE endpoints as your workflow requires for update/removal.

