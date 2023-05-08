import requests
import re

url = "https://evolo.no/om-oss" # crawl target
response = requests.get(url)

if response.status_code == 200:
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", response.text)
    unique_emails = set(emails)
    print("Found the following email addresses on the website:")
    for email in unique_emails:
        print(email)
else:
    print("Failed to crawl website")