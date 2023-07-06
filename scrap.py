import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_product_listings(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    data = []
    for product in products:
        product_url = "https://www.amazon.in" + product.find("a", class_="a-link-normal s-no-outline")["href"]
        product_name = product.find("span", class_="a-size-medium a-color-base a-text-normal").text.strip()
        product_price = product.find("span", class_="a-offscreen").text.strip()
        rating = product.find("span", class_="a-icon-alt").text.strip().split()[0]
        num_reviews = product.find("span", {"class": "a-size-base s-underline-text"}).text.strip().split()[0]
        asin = product["data-asin"]


        data.append({
            "Product URL": product_url,
            "Product Name": product_name,
            "Product Price": product_price,
            "Rating": rating,
            "Number of Reviews": num_reviews,
            "ASIN": asin
        })

    return data

def scrape_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
        

    return {
        # "Product Description": description,
        # "Manufacturer": manufacturer,
    }

def scrape_amazon_data():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"

    all_data = []
    for page in range(1, 21):  # Scraping 20 pages
        url = base_url + str(page)
        print(f"Scraping page {page}...")
        product_listings = scrape_product_listings(url)
        for product in product_listings:
            product_url = product["Product URL"]
            product_details = scrape_product_details(product_url)
            product.update(product_details)
            all_data.append(product)

    df = pd.DataFrame(all_data)
    df.to_csv("amazon_data.csv", index=False)
    print("Data saved to 'amazon_data.csv'")

scrape_amazon_data()
