from pwdlib import PasswordHash
from fastapi import HTTPException
import re

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def password_strength(password: str):
    if len(password)<8:
        raise HTTPException(status_code=400, detail="Password length must be atleast 8 characters.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain atleast 1 digit.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain atleast one uppercase character.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain atleast one lowercase character.")
    if not re.search(r"[~`!@#$%^&*()_+=\[\]{};:'\",.<>?/\\|-]", password):
        raise HTTPException(status_code=400, detail="Password must contain atleast one speicial character.")