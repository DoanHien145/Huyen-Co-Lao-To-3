"""
Module quản lý và tra cứu dữ liệu từ File Excel (.xlsx), CSV (.csv) hoặc Google Sheets.
Giúp Bot tự động cập nhật dữ liệu từ Google Sheets / Excel để trả lời chính xác nhất.
"""

import os
import csv
import time
import urllib.request
from typing import List, Dict, Any
from utils import logger

# Thử import openpyxl để đọc file .xlsx
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1qGL7A7PB0PdJAzaAWGiPECn9eCFWwXWkFsiYD-WHjE4/export?format=csv&gid=1383258709"
AUTO_SYNC_INTERVAL_SEC = 300  # Tự động cập nhật mỗi 5 phút (300 giây)


class KnowledgeManager:
    """Quản lý nạp, tự động đồng bộ và tìm kiếm dữ liệu từ file Excel / CSV hoặc Google Sheets."""

    def __init__(self, file_paths: List[str] = None):
        if file_paths is None:
            self.file_paths = ["knowledge.csv", "data.csv", "data.xlsx", "knowledge.xlsx"]
        else:
            self.file_paths = file_paths
        
        self.records: List[Dict[str, str]] = []
        self.loaded_file: str = ""
        self.last_sync_time: float = 0.0
        self.load_data()

    def sync_google_sheets(self, force: bool = False) -> bool:
        """Tải dữ liệu mới nhất từ Google Sheets về knowledge.csv và data.csv."""
        now = time.time()
        if not force and (now - self.last_sync_time) < AUTO_SYNC_INTERVAL_SEC and self.records:
            return True  # Vẫn còn mới, không cần tải lại

        try:
            req = urllib.request.Request(GOOGLE_SHEET_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode("utf-8")
                if len(content) > 50:
                    with open("knowledge.csv", "w", encoding="utf-8") as f:
                        f.write(content)
                    with open("data.csv", "w", encoding="utf-8") as f:
                        f.write(content)
                    self.last_sync_time = now
                    logger.info("🟢 Đã tự động đồng bộ dữ liệu mới nhất từ Google Sheets!")
                    return True
        except Exception as e:
            logger.warning(f"⚠️ Không thể tải dữ liệu mới từ Google Sheets: {e}")
        return False

    def load_data(self, force_sync: bool = False) -> None:
        """Nạp dữ liệu từ file Excel hoặc CSV đầu tiên tìm thấy."""
        self.sync_google_sheets(force=force_sync)

        self.records = []
        self.loaded_file = ""

        for path in self.file_paths:
            if not os.path.exists(path):
                continue

            try:
                if path.endswith(".xlsx"):
                    if HAS_OPENPYXL:
                        wb = openpyxl.load_workbook(path, data_only=True)
                        sheet = wb.active
                        rows = list(sheet.iter_rows(values_only=True))
                        if rows and len(rows) > 1:
                            headers = [str(h or f"col_{i}").strip() for i, h in enumerate(rows[0])]
                            for r in rows[1:]:
                                if any(r):
                                    row_dict = {}
                                    for i, val in enumerate(r):
                                        if i < len(headers) and val is not None:
                                            v_str = str(val).strip()
                                            if v_str:
                                                row_dict[headers[i]] = v_str
                                    if row_dict:
                                        self.records.append(row_dict)
                            self.loaded_file = path
                            logger.info(f"📊 Đã nạp {len(self.records)} dòng dữ liệu từ Excel: {path}")
                            return
                    else:
                        logger.warning(f"⚠️ Chưa cài openpyxl để đọc {path}. Sẽ dùng CSV.")
                
                elif path.endswith(".csv"):
                    with open(path, mode="r", encoding="utf-8-sig") as f:
                        reader = csv.reader(f)
                        all_rows = list(reader)
                        if len(all_rows) > 1:
                            header_idx = 0
                            for idx, r in enumerate(all_rows):
                                if any(c.strip() for c in r):
                                    header_idx = idx
                                    break
                            headers = [str(h or f"cột_{i}").strip() for i, h in enumerate(all_rows[header_idx])]
                            
                            for row in all_rows[header_idx + 1:]:
                                if any(c.strip() for c in row):
                                    row_dict = {}
                                    for i, val in enumerate(row):
                                        val_str = str(val or "").strip()
                                        if val_str and i < len(headers) and headers[i]:
                                            row_dict[headers[i]] = val_str
                                    if row_dict:
                                        self.records.append(row_dict)
                            
                            self.loaded_file = path
                            logger.info(f"📊 Đã nạp {len(self.records)} dòng dữ liệu từ CSV: {path}")
                            return

            except Exception as e:
                logger.error(f"❌ Lỗi khi đọc file dữ liệu {path}: {e}")

        if not self.loaded_file:
            logger.info("ℹ️ Chưa tìm thấy file Excel/CSV dữ liệu.")

    def search_knowledge(self, query: str, top_k: int = 3) -> str:
        """
        Tìm kiếm thông tin liên quan trong file Excel/CSV (Tự động cập nhật nếu hết hạn 5 phút).
        Sử dụng bộ lọc từ dừng (Stopwords) và Token Budget Guard để TIẾT KIỆM TỐI ĐA TOKEN.
        """
        # Tự động đồng bộ nếu đã quá 5 phút
        if time.time() - self.last_sync_time > AUTO_SYNC_INTERVAL_SEC:
            self.load_data(force_sync=True)

        if not self.records:
            self.load_data()
            if not self.records:
                return ""

        # Lọc các từ dừng vô nghĩa để tìm chính xác tên/Game ID/Zalo
        stopwords = {"là", "gì", "ai", "cho", "hỏi", "xem", "tìm", "tra", "cứu", "của", "tôi", "em", "bot", "với", "được", "không", "nhỉ", "sao", "bao", "nhiêu", "thế", "nào"}
        raw_words = [w.strip().lower() for w in query.split() if len(w.strip()) > 1]
        query_words = [w for w in raw_words if w not in stopwords]

        if not query_words:
            return ""

        scored_records = []
        for record in self.records:
            row_text = " ".join(record.values()).lower()
            score = 0
            for word in query_words:
                if word in row_text:
                    score += 2 if len(word) >= 4 else 1  # Ưu tiên từ khóa dài/đặc trưng
            if score > 0:
                scored_records.append((score, record))

        if not scored_records:
            return ""  # Không tìm thấy kết quả phù hợp -> Tốn 0 token bổ sung!

        scored_records.sort(key=lambda x: x[0], reverse=True)
        top_matches = [rec for _, rec in scored_records[:top_k]]

        formatted_info = [f"=== DỮ LIỆU EXCEL TỪ GOOGLE SHEETS ==="]
        for idx, item in enumerate(top_matches, 1):
            fields = [f"{k}: {v}" for k, v in item.items() if v and k.lower() not in ["stt", "gói"]]
            formatted_info.append(f"[{idx}] " + " | ".join(fields[:6]))  # Chỉ lấy tối đa 6 cột chính
        
        result_text = "\n".join(formatted_info)
        # Giới hạn tối đa ~300 ký tự để tiết kiệm token tối đa
        if len(result_text) > 800:
            result_text = result_text[:800] + "..."

        return result_text


# Singleton instance
knowledge_manager = KnowledgeManager()


