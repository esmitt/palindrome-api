import logging
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
logger = logging.getLogger(__name__)


@router.get("/")
async def root():
    """
    Simple health check endpoint.
    Returns my name :) to verify the API is operational.
    """
    return {"Test": "esmitt"}


@router.post("/detect/", response_model=PalindromeResponse)
async def check_palindrome(palindrome: PalindromeBase, db: Session = Depends(get_db)):
    """
    Check if the provided text is a palindrome.

    This endpoint analyzes the input text to determine if it's a palindrome
    according to the specified language rules (English or Spanish).
    The result is stored in the database for future reference.

    Parameters:
    - palindrome: Object containing the text to check and the language
    - db: Database session dependency

    Returns:
    - PalindromeResponse: Contains the detection ID, result, language, and timestamp
    """
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
    """
    Retrieve palindrome detections with optional filters.

    This endpoint returns a list of palindromes (only successful detections)
    that can be filtered by date range and/or language.

    Parameters:
    - from_date: Optional start date for filtering results
    - to_date: Optional end date for filtering results
    - language: Optional language filter (en or es)
    - db: Database session dependency

    Returns:
    - List[PalindromeQuery]: List of matching palindrome detections
    """
    detections = crud.get_detections(db=db,
                                     language=language,
                                     from_date=from_date,
                                     to_date=to_date)
    return detections


@router.get("/all", response_model=List[PalindromeFull])
async def get_all(db: Session = Depends(get_db)):
    """
    Retrieve all stored records.

    This endpoint returns all records in the database,
    including both successful and unsuccessful detections.

    Parameters:
    - db: Database session dependency

    Returns:
    - List[PalindromeFull]: List of all stored records
    """
    all_records = crud.get_all(db=db)
    logger.info(f"Retrieved {len(all_records)} records from database")
    results = []
    for record in all_records:
        logger.debug(f"Processing record: id={record.id}, language={record.language}")
        results.append(PalindromeFull(id=record.id,
                                      is_palindrome=record.is_palindrome,
                                      language=Language(record.language),
                                      text=record.text,
                                      timestamp=record.timestamp))
    logger.info("Successfully processed all records")
    return results


@router.get("/detections/{detection_id}", response_model=PalindromeQueryById)
async def get_detections_query_by_id(detection_id: int,
                                     db: Session = Depends(get_db)):
    """
    Retrieve a specific detection by ID.

    This endpoint returns detailed information about a single
    palindrome detection record identified by its ID.

    Parameters:
    - detection_id: The ID of the detection record to retrieve
    - db: Database session dependency

    Returns:
    - PalindromeQueryById: Detailed information about the detection

    Raises:
    - HTTPException: 404 error if the detection is not found
    """
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
    """
    Delete a specific detection by ID.

    This endpoint permanently removes a palindrome detection record
    from the database.

    Parameters:
    - detection_id: The ID of the detection record to delete
    - db: Database session dependency

    Returns:
    - DeleteResponse: Success status and message

    Raises:
    - HTTPException: 404 error if the detection is not found
    """
    success = crud.delete_detection(db, detection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Detection not found")
    return DeleteResponse(success=success, message=f"Detection of {detection_id} was deleted successfully")