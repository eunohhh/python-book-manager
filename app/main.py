from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="도서 관리 API",
    description="FastAPI를 사용한 도서 관리 시스템",
    version="1.0.0"
)

# root endpoint
@app.get("/")
def read_root():
    return {"message": "도서 관리 API에 오신 것을 환영합니다!"}

# 도서 목록 조회 (검색 기능 포함)
@app.get("/books", response_model=List[schemas.BookResponse])
def read_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    books = crud.get_books(db, skip=skip, limit=limit, search=search)
    return books

# 특정 도서 조회
@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")
    return db_book

# 도서 생성
@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # ISBN 중복 체크
    if book.isbn:
        db_book = crud.get_book_by_isbn(db, isbn=book.isbn)
        if db_book:
            raise HTTPException(status_code=400, detail="이미 등록된 ISBN입니다")
    
    return crud.create_book(db=db, book=book)

# 도서 수정
@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int, 
    book_update: schemas.BookUpdate, 
    db: Session = Depends(get_db)
):
    # ISBN 중복 체크 (다른 책과 중복되면 안됨)
    if book_update.isbn:  
        existing_book = crud.get_book_by_isbn(db, isbn=book_update.isbn)
        if existing_book is not None and getattr(existing_book, 'id', None) != book_id: 
            raise HTTPException(status_code=400, detail="이미 등록된 ISBN입니다")
    
    db_book = crud.update_book(db, book_id=book_id, book_update=book_update)
    if db_book is None:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")
    return db_book

# 도서 삭제
@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다")
    return db_book

@app.get("/health")
def health_check():
    return {"status": "healthy"}