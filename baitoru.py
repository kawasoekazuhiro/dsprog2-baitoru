import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

url_base = {
    '品川区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/shinagawaku/food/',
    '宮崎市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/miyazakishi/food/'
}

pages = {
    '品川区': 50,
    '宮崎市': 38
}

data = []

def scrape_page(city, url, page):
    print(f"Scraping {city}, Page {page}...")

    time.sleep(5)  # リクエスト間隔を空ける

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {city}, Page {page}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    job_listings = soup.find_all('div', class_='bg02')

    if not job_listings:
        print(f"No job listings found for {city}, Page {page}")
        return

    for job in job_listings:
        # 初期化
        job_stores = None
        job_title = None
        job_location = None
        job_wage = None

        try:
            job_stores = job.find('div', class_="pt02b").find('p').text.strip()
        except AttributeError:
            pass

        try:
            job_title = job.find('div', class_="pt02b").find('span').text.strip()
        except AttributeError:
            pass

        try:
            job_location_list = job.find('div', class_='pt02b').find('ul', class_='ul02').find_all('li')
            job_location = ' '.join([li.text.strip() for li in job_location_list])
        except AttributeError:
            pass

        try:
            job_wage = job.find('div', class_='pt03').find('em').text.strip()
        except AttributeError:
            pass

        data.append({
            '都市名': city, 
            '店舗名': job_stores,
            '仕事名': job_title, 
            '勤務地': job_location, 
            '時給': job_wage
        })

for city, base_url in url_base.items():
    for page in range(1, pages[city] + 1):
        # ページURLの設定
        if page == 1:
            url = base_url
        else:
            url = base_url + f'page{page}/'
        
        scrape_page(city, url, page)
    
    print(f"Completed {city}")

if data:
    df = pd.DataFrame(data)
    df.to_csv('jobs_data.csv', index=False, encoding='utf-8-sig')
    print("Data scraped and saved to jobs_data.csv")
else:
    print("No data was scraped.")

with open('jobs_data.sql', 'w', encoding='utf-8-sig') as f:
    f.write('CREATE TABLE job_listings (\n')
    f.write('    id SERIAL PRIMARY KEY,\n')
    f.write('    city VARCHAR(50),\n')
    f.write('    job_stores VARCHAR(255),\n')
    f.write('    job_title VARCHAR(255),\n')
    f.write('    job_location VARCHAR(255),\n')
    f.write('    job_wage VARCHAR(50)\n')
    f.write(');\n\n')

    f.write('INSERT INTO job_listings (city, job_stores, job_title, job_location, job_wage) VALUES\n')
    
    for i, row in enumerate(data):
        values = f"('{row['都市名']}', '{row['店舗名']}', '{row['仕事名']}', '{row['勤務地']}', '{row['時給']}')"
        if i != len(data) - 1:
            values += ',\n'
        else:
            values += ';\n'
        f.write(values)

print("DDL file created successfully as jobs_data.sql")