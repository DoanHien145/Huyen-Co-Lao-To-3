"""
Module quản lý bộ nhớ lịch sử hội thoại (Memory Management)
Lưu trữ tối đa MAX_MEMORY_MESSAGES (mặc định 20 tin nhắn) cho từng channel Discord.
"""

from typing import Dict, List
import config


class ConversationMemory:
    def __init__(self, max_messages: int = config.MAX_MEMORY_MESSAGES):
        # Lưu trữ lịch sử dạng: { channel_id: [ {"role": "user"/"assistant", "content": "..."}, ... ] }
        self._store: Dict[int, List[Dict[str, str]]] = {}
        self.max_messages: int = max_messages

    def add_message(self, channel_id: int, role: str, content: str) -> None:
        """
        Thêm một tin nhắn vào lịch sử channel.
        Tự động xóa tin nhắn cũ nhất nếu vượt quá max_messages.
        """
        if channel_id not in self._store:
            self._store[channel_id] = []

        self._store[channel_id].append({
            "role": role,
            "content": content
        })

        # Giữ lại tối đa max_messages tin nhắn gần nhất
        if len(self._store[channel_id]) > self.max_messages:
            self._store[channel_id] = self._store[channel_id][-self.max_messages:]

    def get_history(self, channel_id: int) -> List[Dict[str, str]]:
        """
        Lấy danh sách tin nhắn lịch sử của channel.
        Return bản sao list tin nhắn để tránh rò rỉ dữ liệu ngoài ý muốn.
        """
        return list(self._store.get(channel_id, []))

    def clear_history(self, channel_id: int) -> None:
        """Xóa lịch sử hội thoại của một channel cụ thể."""
        if channel_id in self._store:
            self._store[channel_id].clear()

    def get_memory_stats(self, channel_id: int) -> Dict[str, int]:
        """Trả về thống kê bộ nhớ cho logging / debug."""
        history = self._store.get(channel_id, [])
        return {
            "channel_id": channel_id,
            "message_count": len(history),
            "max_capacity": self.max_messages
        }


# Instance toàn cục để import và sử dụng trực tiếp
memory_manager = ConversationMemory()
