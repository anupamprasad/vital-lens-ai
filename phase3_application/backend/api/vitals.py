from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
from database import get_db
from api.auth import get_current_user

router = APIRouter(prefix="/api/v1/vitals", tags=["vitals"])


class VitalRecordRequest(BaseModel):
    heart_rate: float
    spO2: float
    duration: int
    stress_level: int | None = None
    hydration: float | None = None


@router.post("")
def record_vitals(
    req: VitalRecordRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    vit = models.Vitals(
        user_id=current_user.id,
        heart_rate=req.heart_rate,
        heart_rate_confidence=1.0,
        measurement_duration=req.duration,
        measured_at=datetime.utcnow(),
        stress_level=req.stress_level,
        hydration=req.hydration,
    )
    db.add(vit)
    db.commit()
    db.refresh(vit)
    return {
        "id": vit.id,
        "heart_rate": vit.heart_rate,
        "spO2": req.spO2,
        "stress_level": req.stress_level,
        "hydration": req.hydration,
        "measured_at": vit.measured_at,
    }

@router.get("/")
def list_vitals(
    period: str = Query("week", regex="^(week|month|year)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    now = datetime.utcnow()
    if period == "week":
        cutoff = now - timedelta(days=7)
    elif period == "month":
        cutoff = now - timedelta(days=30)
    else:
        cutoff = now - timedelta(days=365)
    vitals = (
        db.query(models.Vitals)
        .filter(models.Vitals.user_id == current_user.id)
        .filter(models.Vitals.measured_at >= cutoff)
        .order_by(models.Vitals.measured_at.asc())
        .all()
    )
    return [
        {
            "heart_rate": v.heart_rate,
            "spO2": getattr(v, 'spO2', None),
            "stress_level": getattr(v, 'stress_level', None),
            "hydration": getattr(v, 'hydration', None),
            "timestamp": v.measured_at.isoformat(),
        }
        for v in vitals
    ]

@router.get("/latest")
def latest_vitals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    v = (
        db.query(models.Vitals)
        .filter(models.Vitals.user_id == current_user.id)
        .order_by(models.Vitals.measured_at.desc())
        .first()
    )
    if not v:
        raise HTTPException(status_code=404, detail="No measurements found")
    return {
        "heart_rate": v.heart_rate,
        "spO2": getattr(v, 'spO2', None),
        "stress_level": getattr(v, 'stress_level', None),
        "hydration": getattr(v, 'hydration', None),
        "timestamp": v.measured_at.isoformat(),
    }
