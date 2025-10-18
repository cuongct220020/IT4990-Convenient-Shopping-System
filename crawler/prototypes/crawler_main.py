import traceback

import streamlit as st

from frontend_config import DOMAIN_PAGE_PER_PAGE
from web_service import WebService

# region: Data and service initialization
if "service" not in st.session_state:
    st.session_state.service = WebService()

# region: Frontend
# --- App setup ---
st.set_page_config(
    page_title="Scraper Dashboard",
    page_icon="🕷️",
    layout="centered",
)

# --- Sidebar / Navigation ---
with st.sidebar:
    st.title("Navigation")
    section = st.radio("Go to", ["Collected", "Add"])

# --- Section: Collected ---
if section == "Collected":
    st.title("🗂️ Collected Domains")
    # Paginated fetch from the database via the WebService
    if "domains_page" not in st.session_state:
        st.session_state.domains_page = 1

    per_page = DOMAIN_PAGE_PER_PAGE
    domain_list = None
    domains: list = []
    service: WebService = st.session_state.service
    try:
        domain_list = service.get_collected_domains(st.session_state.domains_page)
        domains = domain_list.domains
    except RuntimeError as exc:
        st.error(f"Failed to load domains: {exc}")

    # Simple pagination controls
    cols = st.columns([1, 1, 3])
    if cols[0].button("Previous"):
        if st.session_state.domains_page > 1:
            st.session_state.domains_page -= 1
    total_page = domain_list.total_pages if domain_list else 0
    cols[2].markdown(
        f"Page **{min(total_page, st.session_state.domains_page)}**"
        + (f" / {total_page}")
    )
    if cols[1].button("Next"):
        # don't go past total_pages if known
        if not domain_list or st.session_state.domains_page < (
            domain_list.total_pages or 1
        ):
            st.session_state.domains_page += 1

    # Display results
    if domains:
        st.markdown("**Collected Domains:**")
        for d in domains:
            # Domain is a SQLAlchemy object; show the domain string and optional created_at
            created = getattr(d, "created_at", None)
            if created:
                st.markdown(f"- **{d.domain}** — _added {created.date()}_")
            else:
                st.markdown(f"- **{d.domain}**")
    else:
        st.info("No domains collected yet.")

# --- Section: Add ---
elif section == "Add":
    st.title("🌏 Add New Source")
    st.write("You can add a domain **or** a single page URL:")

    domain = st.text_input("Domain", placeholder="e.g. example.com")
    st.markdown("#### OR")
    url = st.text_input("Page URL", placeholder="e.g. https://example.com/article")

    if st.button("Add", type="primary", use_container_width=True):
        if domain or url:
            service: WebService = st.session_state.service
            try:
                if domain:
                    service.database.add_domain(domain)
                    # TODO: Use scrape operations on domain to find and crawl valuable pages
                    st.success(f"✅ Added domain: {domain}")
                else:
                    try:
                        if service.is_page_url_crawled(url):
                            st.info(f"URL already crawled: {url}")
                        else:
                            page = service.crawl_page_url(url)
                            st.success(f"✅ Page {url} updated at {page.updated_at}")
                    except ValueError as e:
                        st.error(
                            f"Failed to add: {e}. Details:\n\n{traceback.format_exc()}"
                        )
            except RuntimeError as exc:
                st.error(f"Failed to add: {exc}")
        else:
            st.warning("Please enter a domain or a URL.")
# endregion: Frontend
