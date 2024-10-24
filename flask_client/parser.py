from typing import List, Optional
from models import ItemModel, IndicatorModel
from sqlalchemy.orm import Session


class Indicator:
    def __init__(self, data: dict):
        self.id: str = data.get('id')
        self.date_first_seen: str = data.get('dateFirstSeen')
        self.date_last_seen: str = data.get('dateLastSeen')
        self.deleted: bool = data.get('deleted', False)
        self.domain: Optional[str] = data.get('domain')


class Item:
    def __init__(self, data: dict):
        self.id: str = data.get('id')
        self.author: Optional[str] = data.get('author')
        self.indicators: List[Indicator] = [Indicator(ind) for ind in data.get('indicators', [])]
        self.is_published: bool = data.get('isPublished', False)
        self.is_tailored: bool = data.get('isTailored', False)
        self.seq_update: int = data.get('seqUpdate')


class DataParser:
    def __init__(self, json_data: dict):
        self.items = [Item(item) for item in json_data.get('items', [])]

    def save_to_database(self, session: Session):
        for item in self.items:
            item_model = ItemModel(id=item.id, author=item.author, is_published=item.is_published,
                                   is_tailored=item.is_tailored, seq_update=item.seq_update)
            session.add(item_model)

            for indicator in item.indicators:
                indicator_model = IndicatorModel(id=indicator.id, domain=indicator.domain, item_id=item.id)
                session.add(indicator_model)

        session.commit()
