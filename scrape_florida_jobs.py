# Scraper for Florida State jobs from jobs.myflorida.com
import csv
import time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://jobs.myflorida.com/search"
PAGE_SIZE = 25


def get_jobs_page(start_row: int) -> List[Dict[str, str]]:
    params = {
        "q": "",
        "sortColumn": "referencedate",
        "sortDirection": "desc",
        "startrow": start_row,
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    jobs = []
    for row in soup.select("tr.data-row"):
        title_link = row.select_one("a.jobTitle-link")
        if not title_link:
            continue
        job = {
            "title": title_link.get_text(strip=True),
            "location": row.select_one("span.jobLocation").get_text(strip=True),
            "date": row.select_one("span.jobDate").get_text(strip=True),
            "department": row.select_one("span.jobDepartment").get_text(strip=True),
            "facility": row.select_one("span.jobFacility").get_text(strip=True),
            "url": requests.compat.urljoin(BASE_URL, title_link["href"]),
        }
        jobs.append(job)
    return jobs


def scrape_all_jobs() -> List[Dict[str, str]]:
    all_jobs = []
    start = 0
    while True:
        jobs = get_jobs_page(start)
        if not jobs:
            break
        all_jobs.extend(jobs)
        start += PAGE_SIZE
        time.sleep(0.2)  # polite delay
    return all_jobs


def write_csv(jobs: List[Dict[str, str]], filename: str = "florida_jobs.csv") -> None:
    if not jobs:
        print("No jobs found")
        return
    keys = sorted({k for job in jobs for k in job.keys()})
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    print(f"Wrote {len(jobs)} jobs to {filename}")


if __name__ == "__main__":
    jobs = scrape_all_jobs()
    write_csv(jobs)
