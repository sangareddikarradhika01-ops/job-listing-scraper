import requests
from bs4 import BeautifulSoup
import csv
url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)

if response.status_code == 200:
    print("Website accessed successfully!")
else:
    print("Failed to access website:", response.status_code)
soup = BeautifulSoup(response.text, "html.parser")
job_cards = soup.find_all("div", class_="card-content")

print("Total jobs found:", len(job_cards))
jobs = []

for job in job_cards:

    title = job.find("h2", class_="title").get_text(strip=True)

    company = job.find(
        "h3", class_="subtitle"
    ).get_text(strip=True)

    location = job.find(
        "p", class_="location"
    ).get_text(strip=True)

    description_tag = job.find("div", class_="content")

    if description_tag:
        description_soup = BeautifulSoup(
            str(description_tag), "html.parser"
        )

        for link in description_soup.find_all("a"):
            link.decompose()

        description = description_soup.get_text(
            " ", strip=True
        )
    else:
        description = ""

    apply_link = ""

    for link in job.find_all("a", href=True):
        if "apply" in link.get_text(strip=True).lower():
            apply_link = link["href"]
            break

    jobs.append({
        "Title": title,
        "Company": company,
        "Location": location,
        "Description": description,
        "Application Link": apply_link
    })

print("Job information extracted successfully!")
with open("jobs.csv", "w", newline="", encoding="utf-8-sig") as file:

    fieldnames = [
        "Title",
        "Company",
        "Location",
        "Description",
        "Application Link"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(jobs)

print("All jobs saved successfully in jobs.csv!")

