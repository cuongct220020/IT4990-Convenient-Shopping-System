"""Communicates with database and backends."""

import os
from datetime import datetime

from firecrawl import Firecrawl
from pydantic import BaseModel
from dotenv import load_dotenv

from utils import is_valid_url, get_url_domain
from data_manager import WebCrawlerDB, CrawlStatus

load_dotenv()

DB_DIR = os.getenv("DB_DIR", "db_dir_missing")
DB_FILENAME = os.getenv("DB_FILENAME", "db_filename_missing")
FIRECRAWL_HOST = os.getenv("FIRECRAWL_HOST", "firecrawl_host_missing")
FIRECRAWL_USE_HTTPS = os.getenv("FIRECRAWL_USE_HTTPS", "false").lower() == "true"
FIRECRAWL_HOST_ADDR = f"{'https' if FIRECRAWL_USE_HTTPS else 'http'}://{FIRECRAWL_HOST}"


class FireCrawlPageMetadata(BaseModel):
    title: str
    description: str
    sourceUrl: str


class FireCrawlPageResponseData(BaseModel):
    markdown: str
    metadata: FireCrawlPageMetadata


class FireCrawlPageResponse(BaseModel):
    success: bool
    data: FireCrawlPageResponseData


class PageDTO(BaseModel):
    class Config:
        from_attributes = True

    content_markdown: str
    updated_at: datetime


class WebService:
    def __init__(self):
        self.database = WebCrawlerDB(DB_DIR, DB_FILENAME)
        self.firecrawl = Firecrawl(api_key="no-key-needed", api_url=FIRECRAWL_HOST_ADDR)

    def get_collected_domains(self, page: int):
        return self.database.get_all_domains(page)

    def is_page_url_crawled(self, url: str) -> bool:
        return self.database.get_page_details(url) is not None

    def crawl_page_url(self, url: str) -> PageDTO:
        if not is_valid_url(url):
            raise ValueError(f"Invalid URL provided: {url}")
        if self.database.get_page_details(url) is None:
            domain = get_url_domain(url)
            if not self.database.domain_exists(domain):
                self.database.add_domain(domain)

            self.database.add_page(url, domain)

            try:
                crawl_result = self.firecrawl.scrape(
                    url,
                    formats=["markdown"],
                    only_main_content=True,
                    fast_mode=False,
                    headers={
                        "User-Agent": "firecrawl-test-agent",
                        "Content-Type": "application/json",
                    },
                )
                is_crawl_failed = (
                    crawl_result.markdown is None or len(crawl_result.markdown) == 0
                )
                if is_crawl_failed:
                    self.database.update_page_status(url, CrawlStatus.FAILED)
                    raise RuntimeError("Crawling failed on the backend.")
                assert crawl_result.markdown is not None
                self.database.save_page_content(url, crawl_result.markdown)
            except ValueError as e:
                self.database.update_page_status(url, CrawlStatus.FAILED)
                raise e

        return PageDTO.model_validate(self.database.get_page_details(url))
