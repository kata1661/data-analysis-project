import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import matplotlib.pyplot as plt

# Setup Chrome options
options = Options()

# Set Firefox user agent to make Chrome look like Firefox
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0"
options.add_argument(f"user-agent={user_agent}")

# Optionally run headless if you want (comment out if you want to see browser)
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

# Path to chromedriver.exe
driver_path = r"c:\Users\katar\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe"
service = Service(driver_path)

# Initialize driver
driver = webdriver.Chrome(service=service, options=options)

# Create WebDriverWait instance AFTER driver initialization
wait = WebDriverWait(driver, 10)

# Open the URL
url = "https://pl.indeed.com/jobs?q=data+analyst&l=Polska&ts=1750014064747&from=searchOnHP&rq=1&rsIdx=0&newcount=1447&fromage=last&vjk=5d9ce598c4e96af8"
driver.get(url)

print("Page title:", driver.title)
print("Current URL:", driver.current_url)
print("Page source snippet:\n", driver.page_source[:1000])  # first 1000 chars

# Wait until at least one job card element appears (use the correct selector!)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon")))

# Optional: sleep a bit more to ensure page fully loaded dynamic content
time.sleep(2)

# Extract job data
titles = []
locations = []

job_cards = driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')

for card in job_cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "a.jcs-JobTitle > span").text
        location = card.find_element(By.CLASS_NAME, 'companyLocation').text
        titles.append(title)
        locations.append(location)
    except Exception as e:
        print(f"Error parsing a job card: {e}")
        continue

# Don't quit driver before scraping is done

# Create DataFrame
df = pd.DataFrame({
    "Job Title": titles,
    "Location": locations
})

print(df.head())

# Plot job title frequency if data exists
if not df.empty:
    df["Job Title"].value_counts().head(10).plot(kind='bar', color='skyblue')
    plt.title("Top 10 Job Titles for Data Analyst")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ No job data found. Try checking your selectors or increasing sleep time.")

# Finally quit driver
driver.quit()
