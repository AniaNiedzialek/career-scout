# Career Scout
A Python script that scrapes LinkedIn for new Software Engineer job postings in the United States and notifies you when new listings appear. Designed for macOS and cross-platform use with optional native notifications.

## Features

- Scrapes job listings from LinkedIn based on query and location
- Detects and filters out already-seen jobs using a local JSON file
- Sends native system notifications for new jobs:
  - macOS: Uses `terminal-notifier` or `osascript`
  - Other systems: Uses `plyer` (if installed)
- Saves job links to avoid duplicate alerts in future runs

---

## Requirements

- Python 3.6 or higher
- `requests`
- `beautifulsoup4`

Optional for notifications:

- macOS:
  ```bash
  brew install terminal-notifier
  ```
- Linux/Windows:
  ```
  pip install plyer
  ```

## Notes
- The script supports both legacy and new LinkedIn job card layouts.
- seen_jobs.json is used to track already-notified jobs between runs.
- Ensure that your system allows notification scripts to run.
The python script was created for personal use only.

