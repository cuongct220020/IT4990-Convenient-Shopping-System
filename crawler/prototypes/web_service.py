"""Communicates with database and backends."""

import os

from data_manager import WebCrawlerDB
from dotenv import load_dotenv

load_dotenv()

DB_DIR = os.getenv("DB_DIR", "db/web_crawler.db")
DB_FILENAME = os.getenv("DB_FILENAME", "db/web_crawler.db")


class WebService:
    def __init__(self):
        self.database = WebCrawlerDB(DB_DIR, DB_FILENAME)

    def get_collected_domains(self, page: int):
        return self.database.get_all_domains(page)
