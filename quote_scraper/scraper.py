import requests
from bs4 import BeautifulSoup
import logging
from time import sleep
from .config import BASE_URL, HEADERS


def fetch_page(url):
    """
    Fetch HTML content from a given URL.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status();
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def scrape_quotes():
    """
    Scrapes quotes from multiple pages of the website and returns them as a list.
    """
    all_quotes = []
    url = "/page/1"

    while url:
        full_url = f"{BASE_URL}{url}"
        logging.info(f"Scraping {full_url}")
        html = fetch_page(full_url)

        if not html:
            logging.error(f"Skipping {full_url} due to fetch failure.")
            break
    
        soup = BeautifulSoup(html, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            try:
                text = quote.find(class_="text").get_text(strip=True)
                author = quote.find(class_="author").get_text(strip=True)
                bio_link = quote.find("a")["href"]
                all_quotes.append({
                    "text": text, 
                    "author": author,
                    "bio_link": bio_link
                })
            except AttributeError as e:
                logging.warning(f"Skipping a malformed quote query: {e}")
        
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        sleep(5)

    return all_quotes

def fetch_author_details(bio_link):
    """
    Fetches additional author details like birth date and place, from the author bio page.
    """ 
    full_url = f"{BASE_URL}{bio_link}"
    html = fetch_page(full_url)

    if not html:
        logging.error(f"Could not fetch author details from {full_url}")
        return None, None
    
    soup = BeautifulSoup(html, "html.parser")

    try:
        birth_date = soup.find(class_="author-born-date").get_text(strip=True)
        birth_place = soup.find(class_="author-born-location").get_text(strip=True)
        return birth_date, birth_place
    except AttributeError:
        logging.warning(f"Could not extract author details from {full_url}")
        return None, None

