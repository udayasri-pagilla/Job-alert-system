import json
import requests
from bs4 import BeautifulSoup
from email_utils import send_email
import os

# --- Load company URLs
with open("companies.json", "r") as f:
    COMPANIES = json.load(f)

# --- Load subscribers
with open("subscribers.json", "r") as f:
    subscribers = json.load(f)

# --- Load notified job IDs
try:
    with open("notified.json", "r") as f:
        notified = set(json.load(f))
except:
    notified = set()

# --- Email config (from GitHub secrets)
from_email = os.environ.get("FROM_EMAIL")
app_password = os.environ.get("APP_PASSWORD")

# --- Main logic
for sub in subscribers:
    user_email = sub["email"]
    user_keywords = sub["keywords"]
    new_jobs = []

    for company in COMPANIES:
        try:
            res = requests.get(company["url"], timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text().lower()

            for keyword in user_keywords:
                job_id = f"{company['name']}-{keyword}-{user_email}"
                if keyword in text and job_id not in notified:
                    new_jobs.append((company["name"], keyword, company["url"]))
                    notified.add(job_id)
        except Exception as e:
            print(f"Error checking {company['name']}: {e}")

    if new_jobs:
        body = f"<h3>Hi {user_email} 👋, here are your job alerts:</h3>"
        for name, keyword, url in new_jobs:
            body += f"<p><b>{name}</b> posted about <i>{keyword}</i><br><a href='{url}'>Apply Here</a></p><hr>"

        send_email("🔥 Job Alerts for You!", body, user_email, from_email, app_password)

# --- Save notified list
with open("notified.json", "w") as f:
    json.dump(list(notified), f)
