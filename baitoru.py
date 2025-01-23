import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

urls = {
    '品川区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/shinagawaku/btp1/',
    '目黒区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/meguroku/btp1/',
    '大田区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/ootaku/btp1/',
    '宮崎市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/miyazakishi/btp1/',
    '都城市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/miyakonojo/btp1/',
    '延岡市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/nobeoka/btp1/'
}

data = []

for city, url in urls.items():
    print(f"Scraping {city}...")
    time.sleep(5)
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {city}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_listings = soup.find_all('div', class_='job-data')
    if not job_listings:
        print(f"No job listings found for {city}")
    
    for job in job_listings:
        try:
            job_title = job.find('h2', class_='job-title').text.strip()
        except AttributeError:
            job_title = None
        try:
            job_location = job.find('div', class_='job-location').text.strip()
        except AttributeError:
            job_location = None
        try:
            job_wage = job.find('div', class_='job-wage').text.strip()
        except AttributeError:
            job_wage = None
        
        data.append({
            '場所': city, 
            '仕事名': job_title, 
            '場所詳細': job_location, 
            '時給': job_wage
        })
    
    print(f"Completed {city}")

if data:
    df = pd.DataFrame(data)
    df.to_csv('jobs_data.csv', index=False, encoding='utf-8-sig')
    print("Data scraped and saved to jobs_data.csv")
else:
    print("No data was scraped.")