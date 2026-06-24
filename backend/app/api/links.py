from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.schemas.link import LinkCreate, LinkOut
from app.models.link import Link
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.shortener import generate_short_code
from app.core.cache import delete_url_cache

router = APIRouter()

@router.post("/create", response_model=LinkOut, status_code=201)
def create_link(link_in: LinkCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if link_in.custom_alias:
        existing = db.query(Link).filter(Link.short_code == link_in.custom_alias).first()
        if existing:
            raise HTTPException(status_code=400, detail="Такой alias уже используется")
        short_code = link_in.custom_alias
    else:
        short_code = generate_short_code()
        while db.query(Link).filter(Link.short_code == short_code).first():
            short_code = generate_short_code()
    expires_at = None
    if link_in.expires_in_days and link_in.expires_in_days > 0:
        expires_at = datetime.utcnow() + timedelta(days=link_in.expires_in_days)
    if link_in.expires_at:
        expires_at = link_in.expires_at
    new_link = Link(
        original_url=str(link_in.original_url),
        short_code=short_code,
        expires_at=expires_at,
        created_by_id=current_user.id
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

@router.get("/list", response_model=List[LinkOut])
def list_links(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    links = db.query(Link).filter(Link.created_by_id == current_user.id).all()
    return links

@router.delete("/delete/{short_code}", status_code=204)
def delete_link(short_code: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    if link.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    db.delete(link)
    db.commit()
    delete_url_cache(short_code)
    return