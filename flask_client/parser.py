from typing import List, Optional

class Indicator:
    def __init__(self, data: dict):
        self.id: str = data.get('id')
        self.date_first_seen: Optional[str] = data.get('dateFirstSeen')
        self.date_last_seen: Optional[str] = data.get('dateLastSeen')
        self.deleted: bool = data.get('deleted', False)
        self.description: Optional[str] = data.get('description')
        self.domain: Optional[str] = data.get('domain')

class Item:
    def __init__(self, data: dict):
        self.id: str = data.get('id')
        self.author: Optional[str] = data.get('author')
        self.company_ids: List[str] = data.get('companyId', [])
        self.indicators: List[Indicator] = [Indicator(ind) for ind in data.get('indicators', [])]
        self.indicator_ids: List[str] = data.get('indicatorsIds', [])
        self.is_published: bool = data.get('isPublished', False)
        self.is_tailored: bool = data.get('isTailored', False)
        self.labels: List[str] = data.get('labels', [])
        self.langs: List[str] = data.get('langs', [])
        self.malware_list: List[str] = data.get('malwareList', [])
        self.seq_update: int = data.get('seqUpdate', 0)

class DataParser:
    def __init__(self, json_data: dict):
        self.count: int = json_data.get('count', 0)
        self.items: List[Item] = [Item(item) for item in json_data.get('items', [])]
        self.seq_update: int = json_data.get('seqUpdate', 0)