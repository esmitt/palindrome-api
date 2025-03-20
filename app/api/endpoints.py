from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.palindrome import Palindrome
from app.db import crud
from app.db.base import get_db
from app.schemas.enums import Language
from app.schemas.palindrome import (
    PalindromeBase,
    PalindromeResponse,
    PalindromeQuery,
    PalindromeQueryById,
    PalindromeFull,
    DeleteResponse
)

router = APIRouter()


@router.get("/")
async def root():
    return {"Test": "esmitt"}


@router.post("/detect/", response_model=PalindromeResponse)
async def check_palindrome(palindrome: PalindromeBase, db: Session = Depends(get_db)):
    is_palindrome = Palindrome(palindrome.text, palindrome.language).is_palindrome()
    db_item = crud.insert_detection(db, palindrome, is_palindrome)

    return PalindromeResponse(
        id=db_item.id,
        is_palindrome=db_item.is_palindrome,
        language=db_item.language,
        timestamp=db_item.timestamp
    )


@router.get("/detections", response_model=List[PalindromeQuery])
async def get_detections_query(from_date: Optional[datetime] = Query(None, description="Filter by date (from)"),
                               to_date: Optional[datetime] = Query(None, description="Filter by date (to)"),
                               language: Optional[Language] = Query(None, description="Filter by language (EN, ES)"),
                               db: Session = Depends(get_db)):
    detections = crud.get_detections(db=db,
                                     language=language,
                                     from_date=from_date,
                                     to_date=to_date)
    return detections


@router.get("/all", response_model=List[PalindromeFull])
async def get_all(db: Session = Depends(get_db)):
    all_records = crud.get_all(db=db)
    results = []
    for record in all_records:
        results.append(PalindromeFull(id=record.id,
                                      is_palindrome=record.is_palindrome,
                                      language=record.language,
                                      text=record.text,
                                      timestamp=record.timestamp))
    return results


@router.get("/detections/{detection_id}", response_model=PalindromeQueryById)
async def get_detections_query_by_id(detection_id: int,
                                     db: Session = Depends(get_db)):
    detection = crud.get_detection(db, detection_id)
    if detection is None:
        raise HTTPException(status_code=404, detail="Detection not found")

    return PalindromeQueryById(id=detection.id,
                               is_palindrome=detection.is_palindrome,
                               language=detection.language,
                               text=detection.text,
                               timestamp=detection.timestamp)


@router.delete("/detections/{detection_id}", response_model=DeleteResponse)
async def delete_detection(detection_id: int,
                           db: Session = Depends(get_db)):
    success = crud.delete_detection(db, detection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Detection not found")
    return DeleteResponse(success=success, message=f"Detection of {detection_id} was deleted successfully")
