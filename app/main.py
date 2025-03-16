from datetime import datetime
import schemas, crud, db
from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from contextlib import asynccontextmanager
from language import Language

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init the database on startup
    db.init_db()
    yield
    # Clean up
    print("Application is shutting down. Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

# Handle any SQLAlchemy-related errors globally
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"info": "A database error occurred."},
    )

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"Error during DB session: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        database.close()


@app.get("/")
async def root():
    return {"Test": "esmitt"}

@app.post("/detect/", response_model=schemas.PalindromeResponse)
async def check_palindrome(palindrome: schemas.PalindromeSchema, db: Session = Depends(get_db)):
    is_palindrome = palindrome.Palindrome(palindrome.text, palindrome.language).is_palindrome()
    db_item = crud.insert_detection(db, palindrome, is_palindrome)

    return schemas.PalindromeResponse(
        id=db_item.id,
        is_palindrome=db_item.is_palindrome,
        language=db_item.language,
        timestamp=db_item.timestamp
    )

@app.get("/detections", response_model=List[schemas.PalindromeQuery])
async def get_detections_query(from_date: Optional[datetime] = Query(None, description="Filter by date (from)"),
                               to_date: Optional[datetime] = Query(None, description="Filter by date (to)"),
                               language: Optional[Language] = Query(None, description="Filter by language (EN, ES)"),
                               db: Session = Depends(get_db)):
    if from_date:
        try:
            from_date = datetime.fromisoformat(from_date.isoformat())
        except ValueError:
            return {"error": "Invalid from_date format. Use ISO 8601 (e.g., '2023-10-27T10:30:00')"}
    if to_date:
        try:
            to_date = datetime.fromisoformat(to_date.isoformat())
        except ValueError:
            return {"error": "Invalid to_date format. Use ISO 8601 (e.g., '2023-10-27T10:30:00')"}

    detections = crud.get_detections(db=db,
                                     language=language,
                                     from_date=from_date,
                                     to_date=to_date)
    return detections

@app.get("/detections/{detection_id}", response_model=schemas.PalindromeQueryById)
async def get_detections_query_by_id(detection_id: int,
                                     db: Session = Depends(get_db)):
    detection = crud.get_detection(db, detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")

    return schemas.PalindromeQueryById(id=detection.id,
                                       is_palindrome=detection.is_palindrome,
                                       language=detection.language,
                                       text=detection.text,
                                       timestamp=detection.timestamp)