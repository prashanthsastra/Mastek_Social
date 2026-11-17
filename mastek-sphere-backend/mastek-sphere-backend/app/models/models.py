import uuid
from datetime import date, datetime, time
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.session import Base

UUIDT = UUID(as_uuid=True)

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    employee_id: Mapped[str] = mapped_column(String(50), unique=True)
    display_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    job_title: Mapped[str | None] = mapped_column(String(150))
    department: Mapped[str | None] = mapped_column(String(150))
    location: Mapped[str | None] = mapped_column(String(150))
    bio: Mapped[str | None] = mapped_column(Text)
    profile_image_url: Mapped[str | None] = mapped_column(Text)
    cover_image_url: Mapped[str | None] = mapped_column(Text)
    user_status: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class Skill(Base):
    __tablename__ = "skills"
    skill_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    skill_name: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class UserSkill(Base):
    __tablename__ = "user_skills"
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"), primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("skills.skill_id"), primary_key=True)
    proficiency_level: Mapped[str | None] = mapped_column(String(30))

class Post(Base):
    __tablename__ = "posts"
    post_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    content: Mapped[str] = mapped_column(Text)
    post_type: Mapped[str] = mapped_column(String(30), default="TEXT")
    media_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class PostLike(Base):
    __tablename__ = "post_likes"
    post_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("posts.post_id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Comment(Base):
    __tablename__ = "comments"
    comment_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("posts.post_id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    comment_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Community(Base):
    __tablename__ = "communities"
    community_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True, default=uuid.uuid4)
    community_name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    image_url: Mapped[str | None] = mapped_column(Text)
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class CommunityMember(Base):
    __tablename__ = "community_members"
    community_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("communities.community_id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"), primary_key=True)
    member_role: Mapped[str] = mapped_column(String(20), default="MEMBER")
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class GoGuide(Base):
    __tablename__ = "go_guides"
    guide_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    content_url: Mapped[str | None] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    keywords: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class LearningContent(Base):
    __tablename__ = "learning_content"
    learning_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    difficulty_level: Mapped[str | None] = mapped_column(String(30))
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    content_url: Mapped[str | None] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class Event(Base):
    __tablename__ = "events"
    event_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    event_date: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time | None] = mapped_column(Time)
    end_time: Mapped[time | None] = mapped_column(Time)
    location: Mapped[str | None] = mapped_column(String(200))
    event_type: Mapped[str | None] = mapped_column(String(50))
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class EventAttendee(Base):
    __tablename__ = "event_attendees"
    event_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("events.event_id"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"), primary_key=True)
    attendee_status: Mapped[str] = mapped_column(String(30))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class RadioShow(Base):
    __tablename__ = "radio_shows"
    show_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class RadioEpisode(Base):
    __tablename__ = "radio_episodes"
    episode_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    show_id: Mapped[uuid.UUID | None] = mapped_column(UUIDT, ForeignKey("radio_shows.show_id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    audio_url: Mapped[str] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class CultureCast(Base):
    __tablename__ = "culture_cast"
    episode_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    media_url: Mapped[str | None] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class Recognition(Base):
    __tablename__ = "recognition"
    recognition_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True, default=uuid.uuid4)
    sender_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    receiver_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    recognition_type: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class SavedItem(Base):
    __tablename__ = "saved_items"
    __table_args__ = (UniqueConstraint("user_id","content_type","content_id"),)
    saved_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    content_type: Mapped[str] = mapped_column(String(50))
    content_id: Mapped[uuid.UUID] = mapped_column(UUIDT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    notification_id: Mapped[uuid.UUID] = mapped_column(UUIDT, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDT, ForeignKey("users.user_id"))
    notification_type: Mapped[str | None] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(UUIDT)
    is_read: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
