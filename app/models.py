from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text)
    summary = Column(String(500))
    extracted_data = Column(JSON)  # Changed from 'metadata' to 'extracted_data'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, summary={self.summary[:50] if self.summary else 'No summary'}...)>"