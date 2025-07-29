import csv
import requests

BASE_URL = "https://www.governmentjobs.com"
AGENCY = "jacksonvillefl"


def get_jobs_page(page: int):
    url = f"{BASE_URL}/careers/{AGENCY}/home/loadJobsOnMaps"
    params = {"page": page}
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"{BASE_URL}/careers/{AGENCY}",
    }
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("jobList", [])


def scrape_all_jobs():
    all_jobs = []
    page = 1
    while True:
        jobs = get_jobs_page(page)
        if not jobs:
            break
        all_jobs.extend(jobs)
        page += 1
    return all_jobs


def write_csv(jobs, filename="jax_jobs.csv"):
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