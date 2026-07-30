"""
Module quản lý dữ liệu tri thức (Đã tắt tính năng Excel theo yêu cầu).
"""

from typing import List, Dict, Any
from utils import logger


class KnowledgeManager:
    """Quản lý dữ liệu tri thức."""

    def __init__(self, file_paths: List[str] = None):
        self.file_paths = file_paths or []
        self.records: List[Dict[str, str]] = []
        self.loaded_file: str = ""

    def sync_google_sheets(self, force: bool = False) -> bool:
        """Đã tắt đồng bộ Google Sheets."""
        return False

    def load_data(self, force_sync: bool = False) -> None:
        """Đã tắt nạp dữ liệu Excel/CSV."""
        self.records = []
        self.loaded_file = ""

    def search_knowledge(self, query: str, top_k: int = 3) -> str:
        """Đã tắt tra cứu dữ liệu Excel để tiết kiệm tối đa token."""
        return ""


# Singleton instance
knowledge_manager = KnowledgeManager()
