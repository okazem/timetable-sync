from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, JSON, DateTime # 1. DateTimeをここに追加
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# SQLiteデータベースの設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./timetable.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserToken(Base):
    __tablename__ = 'user_tokens'
    
    user_id = Column(String, primary_key=True, index=True)
    user_name = Column(String)
    
    token = Column(String, nullable=False)
    refresh_token = Column(String)
    token_uri = Column(String)
    client_id = Column(String)
    client_secret = Column(String)
    scopes = Column(JSON)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)