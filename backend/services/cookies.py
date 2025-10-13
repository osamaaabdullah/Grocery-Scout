from ..models.metro_cookie import MetroChainCookie
from ..schemas.metro_cookie import CookieCreate
from sqlalchemy.orm import Session


def create_metro_cookie(db: Session, data: CookieCreate):
    cookie_instance = MetroChainCookie(**data.model_dump())
    db.add(cookie_instance)
    db.commit()
    db.refresh(cookie_instance)
    return cookie_instance

def get_metro_cookie(db: Session, store_id: int):
    return db.query(MetroChainCookie).filter(MetroChainCookie.store_id == store_id).first()

