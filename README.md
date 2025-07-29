# DCPS Job Scraper

This repository contains a Python script for scraping open jobs from [Duval County Public Schools](https://duvalschools.schoolspring.com/).

## Requirements
- Python 3.12+
- `requests` library (install with `pip install requests`)

## Usage
Run the scraper to download all current job postings and save them to `duval_jobs.csv`:

```bash
python3 scrape_duval_jobs.py
```

The script queries the public SchoolSpring API to retrieve job listings and detailed job information for each posting. Results are written to a CSV file in the repository directory.
