import csv
import time
import requests

BASE_URL = "https://api.schoolspring.com"
DOMAIN = "duvalschools.schoolspring.com"
PAGE_SIZE = 100


def get_jobs_page(page: int):
    url = f"{BASE_URL}/api/Jobs/GetPagedJobsWithSearch"
    params = {
        "domainName": DOMAIN,
        "keyword": "",
        "location": "",
        "category": "",
        "gradelevel": "",
        "jobtype": "",
        "page": page,
        "size": PAGE_SIZE,
        "sortDateAscending": "false",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("value", {}).get("jobsList", [])


def get_job_detail(job_id: int):
    url = f"{BASE_URL}/api/Jobs/{job_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("value", {}).get("jobInfo", {})


def scrape_all_jobs():
    all_jobs = []
    page = 1
    while True:
        jobs = get_jobs_page(page)
        if not jobs:
            break
        for job in jobs:
            detail = get_job_detail(job["jobId"])
            merged = {**job, **detail}
            all_jobs.append(merged)
            time.sleep(0.1)  # be polite
        page += 1
    return all_jobs


def write_csv(jobs, filename="duval_jobs.csv"):
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
