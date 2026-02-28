"""
Database Models for Vital Lens AI
SQLAlchemy models for PostgreSQL
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))  # M, F, Other
    skin_tone = Column(String(50))  # Fitzpatrick scale
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    # Role flags
    # `is_admin` will allow certain users to access administrative endpoints
    # such as listing all users. It defaults to False for normal accounts.
    is_admin = Column(Boolean, default=False)
    email_verified_at = Column(DateTime)
    
    # 2FA
    totp_secret = Column(String(32))
    totp_enabled = Column(Boolean, default=False)
    
    # Consent & Privacy
    gdpr_consent = Column(Boolean, default=False)
    gdpr_consent_date = Column(DateTime)
    hipaa_acknowledgement = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    vitals = relationship("Vitals", back_populates="user")
    health_records = relationship("HealthRecord", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class Vitals(Base):
    """Heart Rate and Vitals measurements"""
    __tablename__ = "vitals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Measurements
    heart_rate = Column(Float, nullable=False)  # BPM
    heart_rate_confidence = Column(Float, default=0.0)  # 0-1 confidence score
    
    # Signal Quality
    signal_quality = Column(Float)  # 0-1
    measurement_duration = Column(Integer)  # seconds
    
    # Video metadata
    video_filename = Column(String(255))
    video_processed = Column(Boolean, default=False)
    
    # Environmental conditions
    ambient_light = Column(Float)  # lux
    temperature = Column(Float)  # celsius
    humidity = Column(Float)  # percentage
    
    # Device info
    device_type = Column(String(100))  # iPhone, Android, Web
    device_model = Column(String(100))
    app_version = Column(String(50))

    # additional vitals added later (not used by initial rPPG simulation)
    stress_level = Column(Integer, nullable=True)
    hydration = Column(Float, nullable=True)  # percentage 0-100
    
    # Timestamps
    measured_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    deleted_at = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="vitals")


class HealthRecord(Base):
    """User health history and conditions"""
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Medical history
    conditions = Column(Text)  # JSON list of conditions
    medications = Column(Text)  # JSON list of medications
    allergies = Column(Text)  # JSON list of allergies
    
    # Vital baselines
    resting_heart_rate = Column(Float)
    blood_pressure_systolic = Column(Float)
    blood_pressure_diastolic = Column(Float)
    
    # Notes
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="health_records")


class AuditLog(Base):
    """Audit logging for HIPAA/GDPR compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Action details
    action = Column(String(100), index=True)  # "READ", "CREATE", "UPDATE", "DELETE", "EXPORT"
    resource_type = Column(String(50))  # "USER", "VITALS", "HEALTH_RECORD"
    resource_id = Column(String(255))
    
    # Details
    details = Column(Text)  # JSON with additional context
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = relationship("User", back_populates="audit_logs")


class Consent(Base):
    """GDPR consent tracking"""
    __tablename__ = "consents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Consent types
    processing_consent = Column(Boolean, default=False)
    storage_consent = Column(Boolean, default=False)
    third_party_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    
    # Versions
    consent_version = Column(String(20))
    
    # Timestamps
    accepted_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime)  # For periodic reconfirmation


class Session(Base):
    """User session tracking"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Session data
    token = Column(String(500), unique=True, index=True)
    refresh_token = Column(String(500), unique=True)
    
    # Device info
    device_fingerprint = Column(String(255))
    device_name = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_activity = Column(DateTime, default=datetime.utcnow)
    logged_out_at = Column(DateTime)


class DataExport(Base):
    """Track GDPR data export requests"""
    __tablename__ = "data_exports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Export details
    format = Column(String(20))  # JSON, CSV, PDF
    status = Column(String(20), default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED
    
    # Files
    file_path = Column(String(500))
    file_size = Column(Integer)
    
    # Timestamps
    requested_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    expires_at = Column(DateTime)  # Data retention policy


class AppLog(Base):
    """Application logging"""
    __tablename__ = "app_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20))  # INFO, WARNING, ERROR, CRITICAL
    message = Column(Text)
    context = Column(Text)  # JSON
    stack_trace = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


# Create all tables
if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://user:password@localhost/vital_lens_ai")
    Base.metadata.create_all(engine)
    print("✓ Database tables created successfully")
