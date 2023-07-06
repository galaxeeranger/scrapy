import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set the path to the ChromeDriver executable
chrome_driver_path = '"C:\chromedriver.exe"'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode, if desired

# Set up the ChromeDriver service
service = Service(chrome_driver_path)

# Create a new instance of the ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the target URL
url = 'https://www.amazon.in/Skybags-Brat-Black-Casual-Backpack/dp/B08Z1HHHTD/ref=sr_1_1?crid=2M096C61O4MLT&keywords=bags&qid=1688634604&sprefix=ba%2Caps%2C283&sr=8-1#customerReviews'
driver.get(url)

# Find and extract the ASIN
asin_element = driver.find_element(By.CSS_SELECTOR, '[data-asin]')
asin = asin_element.get_attribute('data-asin')

# Find and extract the manufacturer
manufacturer_element = driver.find_element(By.ID, 'bylineInfo')
manufacturer = manufacturer_element.text.strip()

# Find and extract the product description
description_element = driver.find_element(By.ID, 'productDescription')
description = description_element.text.strip()

# Create or open the CSV file in append mode
csv_file_path = 'amazon_data1.csv'
with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Append the data to the CSV file
    writer.writerow([asin, manufacturer, description, url])

# Close the browser and quit the driver
driver.quit()
