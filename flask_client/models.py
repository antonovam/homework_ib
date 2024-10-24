from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class IndicatorModel(Base):
    __tablename__ = 'indicators'

    id = Column(String, primary_key=True)
    domain = Column(String)
    item_id = Column(String, ForeignKey('items.id'))


class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(String, primary_key=True)
    author = Column(String)
    is_published = Column(Boolean)
    is_tailored = Column(Boolean)
    seq_update = Column(Integer)
    indicators = relationship('IndicatorModel', backref='item')
