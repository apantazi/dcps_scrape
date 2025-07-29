# DCPS Job Scraper

This repository contains Python scripts for scraping job postings from public sources.

* `scrape_duval_jobs.py` – scrape open jobs from [Duval County Public Schools](https://duvalschools.schoolspring.com/).
* `scrape_florida_jobs.py` – scrape listings from [State of Florida Careers](https://jobs.myflorida.com/search).

## Requirements
- Python 3.12+
- `requests` library (install with `pip install requests`)

## Usage
Run one of the scrapers to download current job postings and save them to a CSV file.

Duval County Public Schools:

```bash
python3 scrape_duval_jobs.py
```

State of Florida Careers:

```bash
python3 scrape_florida_jobs.py
```

Each script writes all retrieved listings to a CSV file in the repository directory.
