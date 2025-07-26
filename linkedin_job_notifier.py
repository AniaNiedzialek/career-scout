import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import platform
import subprocess
# from plyer import notification  # Only use for non-macOS

SEARCH_URL = "https://www.linkedin.com/jobs/search/"
QUERY = "Software Engineer"
LOCATION = "United States"
SEEN_JOBS_FILE = "seen_jobs.json"

# On macOS, install terminal-notifier for clickable notifications:
#   brew install terminal-notifier

def get_job_listings():
    params = {
        'keywords': QUERY,
        'location': LOCATION,
        'trk': 'public_jobs_jobs-search-bar_search-submit',
        'position': 1,
        'pageNum': 0
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    for job_card in soup.find_all('li', class_='result-card job-result-card result-card--with-hover-state'):
        title_tag = job_card.find('h3', class_='result-card__title job-result-card__title')
        company_tag = job_card.find('h4', class_='result-card__subtitle job-result-card__subtitle')
        location_tag = job_card.find('span', class_='job-result-card__location')
        link_tag = job_card.find('a', class_='result-card__full-card-link')
        if title_tag and company_tag and location_tag and link_tag:
            job = {
                'title': title_tag.get_text(strip=True),
                'company': company_tag.get_text(strip=True),
                'location': location_tag.get_text(strip=True),
                'link': link_tag['href']
            }
            jobs.append(job)
    # Fallback for new LinkedIn layout
    if not jobs:
        for job_card in soup.find_all('div', class_='base-card'):
            title_tag = job_card.find('h3', class_='base-search-card__title')
            company_tag = job_card.find('h4', class_='base-search-card__subtitle')
            location_tag = job_card.find('span', class_='job-search-card__location')
            link_tag = job_card.find('a', class_='base-card__full-link')
            if title_tag and company_tag and location_tag and link_tag:
                job = {
                    'title': title_tag.get_text(strip=True),
                    'company': company_tag.get_text(strip=True),
                    'location': location_tag.get_text(strip=True),
                    'link': link_tag['href']
                }
                jobs.append(job)
    return jobs

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        try:
            with open(SEEN_JOBS_FILE, 'r') as f:
                return set(json.load(f))
        except json.decoder.JSONDecodeError:
            print(f"Error decoding {SEEN_JOBS_FILE}. Deleting it to create a new one.")
            os.remove(SEEN_JOBS_FILE)
            return set()
    return set()

def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_FILE, 'w') as f:
        json.dump(list(seen_jobs), f)

def notify_new_job(job):
    title = f"New Job: {job['title']}"
    message = f"{job['company']} - {job['location']}"
    url = job['link']
    if platform.system() == "Darwin":
        print("Sending notification for:", url)   # Use terminal-notifier for clickable notifications
        try:
            subprocess.run([
                "terminal-notifier",
                "-title", title,
                "-message", message,
                "-open", url,
                "-appIcon", "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarAdvanced.icns"
            ])
        except FileNotFoundError:
            # Fallback to osascript if terminal-notifier is not installed
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script])
    else:
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_name="Job Notifier",
                timeout=10
            )
        except ImportError:
            print("plyer not installed, cannot show notification.")
    print(f"=======================")
    print(f"New job: {job['title']} at {job['company']} ({job['location']})\n{job['link']}")

def main():
    jobs = get_job_listings()
    seen_jobs = load_seen_jobs()
    new_jobs = []
    for job in jobs:
        job_id = job['link']
        if job_id not in seen_jobs:
            notify_new_job(job)
            new_jobs.append(job_id)
    if new_jobs:
        seen_jobs.update(new_jobs)
        save_seen_jobs(seen_jobs)
    if not new_jobs:
        print("No new jobs found today.")

if __name__ == "__main__":
    main() 