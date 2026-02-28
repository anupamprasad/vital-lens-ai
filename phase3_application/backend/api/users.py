from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
from database import get_db
from api.auth import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/me")
def get_profile(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "name": current_user.username}

@router.patch("/me")
def update_profile(name: str | None = None, email: str | None = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if name:
        current_user.username = name
    if email and email != current_user.email:
        if db.query(models.User).filter(models.User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = email
    db.commit()
    return {"message": "Profile updated"}

@router.post("/me/password")
def change_password(old_password: str, new_password: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    from ..auth_utils import verify_password, get_password_hash
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    current_user.password_hash = get_password_hash(new_password)
    db.commit()
    return {"message": "Password updated"}

@router.delete("/me")
def delete_account(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted"}


@router.get("/")
def list_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Return a list of all users.

    Admins may eventually be required to view the full list, but for now
    any authenticated user can call this endpoint for debugging/demo.

    The response purposely omits sensitive fields such as password_hash.
    """

    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin privileges required")

    users = db.query(models.User).all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "email": u.email,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "is_admin": getattr(u, "is_admin", False),
            "created_at": u.created_at,
        })
    return result
