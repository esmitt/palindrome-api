from sqlalchemy.orm import Session
from sqlalchemy import cast, String, Boolean, Integer

from app.models import PalindromeRecord
from schemas import PalindromeBase, PalindromeQuery
import models
from typing import Optional, Type
from datetime import datetime
from palindrome import Language

def insert_detection(db: Session,
                     palindrome: PalindromeBase,
                     is_palindrome: bool) -> models.PalindromeRecord:
    # the timestamp is set at this point
    db_item = models.PalindromeRecord(text=palindrome.text,
                                      language=palindrome.language.value,
                                      is_palindrome=is_palindrome)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_detections(db: Session,
                   language: Optional[Language] = None,
                   from_date: Optional[datetime] = None,
                   to_date: Optional[datetime] = None) -> list[PalindromeQuery]:
    query = db.query(models.PalindromeRecord)

    # important: get words which are palindrome
    query = query.where(cast(models.PalindromeRecord.is_palindrome, Boolean) == True)

    if language:
        query = query.filter(cast(models.PalindromeRecord.language, String) == language.value)
    if from_date:
        query = query.filter(models.PalindromeRecord.timestamp >= from_date)
    if to_date:
        query = query.filter(models.PalindromeRecord.timestamp <= to_date)

    result = []
    for record in query.all():
        result.append(PalindromeQuery(
            id=record.id,
            text=record.text,
            timestamp=record.timestamp,
            language=Language(record.language)
        ))
    return result

def get_all(db: Session) -> list[Type[PalindromeRecord]]:
    return db.query(models.PalindromeRecord).all()

def get_detection(db: Session,
                  detection_id: int) -> Optional[models.PalindromeRecord]:
    query = db.query(models.PalindromeRecord).filter(cast(models.PalindromeRecord.id, Integer) == detection_id)
    return query.first()

def delete_detection(db: Session,
                     detection_id: int) -> bool:
    query = db.query(models.PalindromeRecord).filter(cast(models.PalindromeRecord.id, Integer) == detection_id).first()

    if query is None:
        return False

    db.delete(query)
    db.commit()
    return True