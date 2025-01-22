import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 対象となるURLのリスト
urls = {
    '品川区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/shinagawaku/',
    '目黒区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/meguroku/',
    '大田区': 'https://www.baitoru.com/kanto/jlist/tokyo/23ku/ootaku/',
    '宮崎市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/miyazakishi/',
    '都城市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/miyakonojo/',
    '延岡市': 'https://www.baitoru.com/kyushu/jlist/miyazaki/nobeoka/'
}

# データのリスト
data = []

# 各市町村のページをループ
for city, url in urls.items():
    print(f"Scraping {city}...")
    
    # サーバに負荷をかけないように
    time.sleep(5)
    
    # URLにHTTPリクエストを送信
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 求人情報を抽出（具体的なパーサーはサイト構造に応じて変更が必要）
    job_listings = soup.find_all('div', class_='job-data')
    
    for job in job_listings:
        job_title = job.find('h2', class_='job-title').text.strip()
        job_location = job.find('div', class_='job-location').text.strip()
        job_wage = job.find('div', class_='job-wage').text.strip()
        
        # データをリストに追加
        data.append({'場所': city, '仕事名': job_title, '場所詳細': job_location, '時給': job_wage})
    
    print(f"Completed {city}")

# データフレームに変換
df = pd.DataFrame(data)

# データをCSVファイルとして保存
df.to_csv('jobs_data.csv', index=False, encoding='utf-8-sig')

print("Data scraped and saved to jobs_data.csv")