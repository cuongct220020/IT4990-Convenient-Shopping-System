"""Manage domains and page information."""

import os
from datetime import datetime, timezone
from enum import Enum
from math import ceil
from dataclasses import dataclass

from sqlalchemy import (
    create_engine,
    String,
    Text,
    ForeignKey,
    Enum as SQLEnum,
    select,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass


class CrawlStatus(str, Enum):
    QUEUED = "queued"
    CRAWLING = "crawling"
    COMPLETED = "completed"
    FAILED = "failed"


class Domain(Base):
    __tablename__ = "domains"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # Relationship
    pages: Mapped[list["Page"]] = relationship(
        back_populates="domain_obj", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Domain(id={self.id}, domain='{self.domain}')>"


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)
    domain_id: Mapped[int] = mapped_column(ForeignKey("domains.id"), index=True)
    status: Mapped[CrawlStatus] = mapped_column(
        SQLEnum(CrawlStatus), default=CrawlStatus.QUEUED, index=True
    )
    content_markdown: Mapped[str | None] = mapped_column(Text, default=None)
    title: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    # Relationships
    domain_obj: Mapped["Domain"] = relationship(back_populates="pages")
    crawl_history: Mapped[list["CrawlHistory"]] = relationship(
        back_populates="page", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Page(id={self.id}, url='{self.url}', status='{self.status}')>"


class CrawlHistory(Base):
    __tablename__ = "crawl_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), index=True)
    status: Mapped[str] = mapped_column(String)
    crawled_at: Mapped[datetime] = mapped_column(default=func.now())
    response_code: Mapped[int | None] = mapped_column(default=None)
    error_message: Mapped[str | None] = mapped_column(Text, default=None)
    content_size: Mapped[int | None] = mapped_column(default=None)
    crawl_duration_ms: Mapped[int | None] = mapped_column(default=None)

    # Relationship
    page: Mapped["Page"] = relationship(back_populates="crawl_history")

    def __repr__(self) -> str:
        return f"<CrawlHistory(id={self.id}, page_id={self.page_id}, status='{self.status}')>"


@dataclass
class Statistics:
    """Statistics of recorded domains and pages."""

    total_pages: int
    queued: int
    crawling: int
    completed: int
    failed: int
    total_domains: int


@dataclass
class DomainList:
    """Paginated list of domains."""

    page: int
    per_page: int
    total: int
    total_pages: int
    domains: list[Domain]


class WebCrawlerDB:
    def __init__(self, db_dir: str, db_filename: str = "crawler.db"):
        os.makedirs(db_dir, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{os.path.join(db_dir, db_filename)}")
        Base.metadata.create_all(self.engine)

    def add_domain(self, domain: str) -> Domain:
        """Add a domain and return the domain object."""
        with Session(self.engine) as session:
            stmt = select(Domain).where(Domain.domain == domain)
            existing = session.scalar(stmt)
            if existing:
                return existing

            new_domain = Domain(domain=domain)
            session.add(new_domain)
            session.commit()
            session.refresh(new_domain)
            return new_domain

    def add_page(
        self, url: str, domain: str, status: CrawlStatus = CrawlStatus.QUEUED
    ) -> Page:
        """Add a page to the queue."""
        with Session(self.engine) as session:
            stmt = select(Page).where(Page.url == url)
            existing = session.scalar(stmt)
            if existing:
                return existing

            domain_obj = self.add_domain(domain)
            new_page = Page(url=url, domain_id=domain_obj.id, status=status)
            session.add(new_page)
            session.commit()
            session.refresh(new_page)
            return new_page

    def update_page_status(self, url: str, status: CrawlStatus) -> None:
        """Update the status of a page."""
        with Session(self.engine) as session:
            stmt = select(Page).where(Page.url == url)
            page = session.scalar(stmt)
            if page:
                page.status = status
                page.updated_at = datetime.now(timezone.utc)
                session.commit()

    def save_page_content(
        self, url: str, markdown: str, title: str | None = None
    ) -> None:
        """Save the crawled content of a page."""
        with Session(self.engine) as session:
            stmt = select(Page).where(Page.url == url)
            page = session.scalar(stmt)
            if page:
                page.content_markdown = markdown
                page.title = title
                page.status = CrawlStatus.COMPLETED
                page.updated_at = datetime.utcnow()
                session.commit()

    def add_crawl_history(
        self,
        page_id: int,
        status: str,
        response_code: int | None = None,
        error_message: str | None = None,
        content_size: int | None = None,
        crawl_duration_ms: int | None = None,
    ) -> None:
        """Add a crawl history entry."""
        with Session(self.engine) as session:
            history = CrawlHistory(
                page_id=page_id,
                status=status,
                response_code=response_code,
                error_message=error_message,
                content_size=content_size,
                crawl_duration_ms=crawl_duration_ms,
            )
            session.add(history)
            session.commit()

    def get_pages_by_status(self, status: CrawlStatus) -> list[Page]:
        """Get all pages with a specific status."""
        with Session(self.engine) as session:
            stmt = select(Page).where(Page.status == status)
            return list(session.scalars(stmt).all())

    def get_pages_by_domain(self, domain: str) -> list[Page]:
        """Get all pages for a specific domain."""
        with Session(self.engine) as session:
            stmt = select(Domain).where(Domain.domain == domain)
            domain_obj = session.scalar(stmt)
            if domain_obj:
                return list(domain_obj.pages)
            return []

    def get_page_details(self, url: str) -> Page | None:
        """Get details of a specific page."""
        with Session(self.engine) as session:
            stmt = select(Page).where(Page.url == url)
            return session.scalar(stmt)

    def get_crawl_history(self, url: str) -> list[CrawlHistory]:
        """Get crawl history for a specific page."""
        with Session(self.engine) as session:
            stmt = select(Page).where(Page.url == url)
            page = session.scalar(stmt)
            if page:
                return sorted(
                    page.crawl_history, key=lambda x: x.crawled_at, reverse=True
                )
            return []

    def get_stats(self) -> Statistics:
        """Get overall crawling statistics."""
        with Session(self.engine) as session:
            total_pages = session.scalar(select(func.count()).select_from(Page))
            queued = session.scalar(
                select(func.count())
                .select_from(Page)
                .where(Page.status == CrawlStatus.QUEUED)
            )
            crawling = session.scalar(
                select(func.count())
                .select_from(Page)
                .where(Page.status == CrawlStatus.CRAWLING)
            )
            completed = session.scalar(
                select(func.count())
                .select_from(Page)
                .where(Page.status == CrawlStatus.COMPLETED)
            )
            failed = session.scalar(
                select(func.count())
                .select_from(Page)
                .where(Page.status == CrawlStatus.FAILED)
            )
            total_domains = session.scalar(select(func.count()).select_from(Domain))

            return Statistics(
                total_pages=total_pages or 0,
                queued=queued or 0,
                crawling=crawling or 0,
                completed=completed or 0,
                failed=failed or 0,
                total_domains=total_domains or 0,
            )

    def get_all_domains(self, page: int = 1, per_page: int = 20) -> DomainList:
        """Get paginated domains, newest first."""
        with Session(self.engine) as session:
            total = session.scalar(select(func.count()).select_from(Domain)) or 0
            total_pages = ceil(total / per_page) if per_page > 0 else 1

            stmt = (
                select(Domain)
                .order_by(Domain.created_at.desc())
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            domains = list(session.scalars(stmt).all())
            return DomainList(
                page=page,
                per_page=per_page,
                total=total,
                total_pages=total_pages,
                domains=domains,
            )
