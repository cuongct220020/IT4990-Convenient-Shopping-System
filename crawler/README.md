This is where we describe the purpose and instructions of the web crawler

# Architecture overview

There are 3 main components in this web crawler service:
* Firecrawl: Get markdown of a web page or a domain's pages
* LLM service: Transform crawled textual data to structured data by using LLM
* Scheduler & manager: Provide interface for to crawl a web page or domain, record the result and later fetch them to the LLM service

# Launch instructions

## How to run locally

**Presequites:**

* Docker installed
* git
* Python `>=3.12`

1. Initialize git submodules:

```sh
# We are here: ./crawler
git submodule update --init --remote --recursive
```

2. Build and run the Firecrawl Docker image:

```sh
# We are here: ./crawler
cd firecrawl
# After copying the file, you can modify it to config Firecrawl service
cp firecrawl/apps/api/.env.example firecrawl/apps/api/.env
# This command is only needed in the first time
docker-compose build
# Run the container
docker-compose up -d
```

3. Create and activate python environments and install dependencies, then start the scheduler service:

```sh
# We are here: ./crawler
python -m venv .venv
source .venv/bin/activate
# Or if you use Windows Powershell
# .venv/Scripts/Activate.ps1
pip install -r requirements.txt
# After copying the file, you can modify it to config the service
cp prototypes/.env.example prototypes/.env
streamlit run prototypes/crawler_main.py
```