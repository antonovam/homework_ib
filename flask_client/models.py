from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()

class IndicatorModel(Base):
    __tablename__ = 'indicators'

    id = Column(String, primary_key=True)
    date_first_seen = Column(String)
    date_last_seen = Column(String)
    deleted = Column(Boolean, default=False)
    description = Column(String)
    domain = Column(String)
    item_id = Column(String, ForeignKey('items.id'))

class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True)
    author = Column(String)
    company_ids = Column(JSON)  # Stored as JSON array
    indicator_ids = Column(JSON)  # Stored as JSON array of indicator IDs
    is_published = Column(Boolean)
    is_tailored = Column(Boolean)
    labels = Column(JSON)  # Stored as JSON array of labels
    langs = Column(JSON)  # Stored as JSON array of languages
    seq_update = Column(Integer)
    malware_list = Column(JSON)  # Store malwareList as a JSON array

    indicators = relationship('IndicatorModel', backref='item', cascade="all, delete-orphan")