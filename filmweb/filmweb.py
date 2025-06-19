from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium driver (make sure chromedriver is in PATH)
driver = webdriver.Chrome()
driver.get("https://www.filmweb.pl/ranking/serial")
time.sleep(5)  # Wait for page to fully load

soup = BeautifulSoup(driver.page_source, 'html.parser')
movies = soup.select('div.rankingType')  # Updated selector

data_list = []

for movie in movies:
    title_tag = movie.select_one('[itemprop="name"]')
    year_tag = movie.select_one('.rankingType__year')
    rating_tag = movie.select_one('.rankingType__rate')

    title = title_tag.text.strip() if title_tag else "N/A"
    year = year_tag.text.strip() if year_tag else "N/A"
    rating = rating_tag.text.strip() if rating_tag else "N/A"

    data_list.append({
        "movie_title": title,
        "year": year,
        "rating": rating
    })

driver.quit()

# Print and save
for movie in data_list:
    print(f"{movie['movie_title']} ({movie['year']}) - Rating: {movie['rating']}")

pd.DataFrame(data_list).to_csv("filmweb_serials.csv", index=False)
print("Done!")
