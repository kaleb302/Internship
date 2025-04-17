# ai/job_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(location):
    url = f"https://www.indeed.com/jobs?q=internship&l={location}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job in soup.find_all('div', class_='job_seen_beacon'):
        title = job.find('h2').text.strip()
        company = job.find('span', class_='companyName').text.strip()
        link = "https://indeed.com" + job.find('a')['href']
        jobs.append({"title": title, "company": company, "link": link})
    
    return jobs
    