"""
AVTech Platform - Database Models
=================================

SQLAlchemy models for the AVTech Platform database.
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()


class Client(Base):
    """Client model for multi-tenant support."""
    __tablename__ = "clients"
    
    client_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False, unique=True)
    api_key = Column(String(255), nullable=False, unique=True)
    storage_limit_bytes = Column(Integer, default=1073741824)  # 1GB default
    storage_used_bytes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    videos = relationship("Video", back_populates="client")
    screens = relationship("Screen", back_populates="client")
    schedule_rules = relationship("ScheduleRule", back_populates="client")


class Video(Base):
    """Video model for content management."""
    __tablename__ = "videos"
    
    video_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    duration_seconds = Column(Integer, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    file_path = Column(String(500), nullable=False)
    hash_sha256 = Column(String(64), nullable=False, unique=True)
    status = Column(String(20), default="uploaded")  # uploaded, processing, ready, error
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.client_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="videos")
    time_slots = relationship("TimeSlot", back_populates="video")


class Screen(Base):
    """Screen model for device management."""
    __tablename__ = "screens"
    
    screen_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    location = Column(String(500))
    screen_code = Column(String(100), nullable=False, unique=True)
    status = Column(String(20), default="offline")  # online, offline, error
    last_heartbeat = Column(DateTime)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.client_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="screens")
    time_slots = relationship("TimeSlot", back_populates="screen")


class ScheduleRule(Base):
    """Schedule rule model for content programming."""
    __tablename__ = "schedule_rules"
    
    rule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    rule_type = Column(String(20), nullable=False)  # daily, weekly, date_range
    active_from = Column(DateTime, nullable=False)
    active_until = Column(DateTime)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.client_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="schedule_rules")
    time_slots = relationship("TimeSlot", back_populates="schedule_rule")


class TimeSlot(Base):
    """Time slot model for scheduling."""
    __tablename__ = "time_slots"
    
    slot_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
    start_time = Column(String(5), nullable=False)  # HH:MM format
    end_time = Column(String(5), nullable=False)    # HH:MM format
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.video_id"), nullable=False)
    screen_id = Column(UUID(as_uuid=True), ForeignKey("screens.screen_id"), nullable=False)
    schedule_rule_id = Column(UUID(as_uuid=True), ForeignKey("schedule_rules.rule_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="time_slots")
    screen = relationship("Screen", back_populates="time_slots")
    schedule_rule = relationship("ScheduleRule", back_populates="time_slots")


class PlayerSyncStatus(Base):
    """Player sync status model for tracking synchronization."""
    __tablename__ = "player_sync_status"
    
    sync_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    screen_code = Column(String(100), nullable=False, unique=True)
    desired_state_version = Column(Integer, nullable=False)
    applied_state_version = Column(Integer)
    last_sync_attempt = Column(DateTime)
    last_successful_sync = Column(DateTime)
    sync_status = Column(String(20), default="pending")  # pending, in_progress, success, failed
    error_message = Column(Text)
    last_heartbeat = Column(DateTime)
    health_metrics = Column(JSON)  # Store CPU, RAM, disk usage, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.client_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client")


class AuditLog(Base):
    """Audit log model for tracking changes."""
    __tablename__ = "audit_logs"
    
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, etc.
    table_name = Column(String(100), nullable=False)
    record_id = Column(String(100), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")