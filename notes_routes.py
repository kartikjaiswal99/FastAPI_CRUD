from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from auth import get_db, get_current_user
from database import Note, User
from schemas import NoteCreate, NoteUpdate, NoteResponse
from datetime import datetime

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Create a new note"""
    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=List[NoteResponse])
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all notes for the authenticated user"""
    notes = db.query(Note).filter(Note.owner_id == current_user.id).all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific note by ID"""
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.owner_id == current_user.id
    ).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a note with version checking to prevent race conditions"""
    db_note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Check version to prevent concurrent updates
    if db_note.version != note_update.version:
        raise HTTPException(
            status_code=409, 
            detail=f"Version conflict. Current: {db_note.version}, provided: {note_update.version}"
        )
    
    # Update note
    db_note.title = note_update.title
    db_note.content = note_update.content
    db_note.version += 1
    db_note.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a note"""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
