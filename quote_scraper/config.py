import logging


BASE_URL = "https://quotes.toscrape.com" # Base URL for scraping
HEADERS = {"User-Agent": "Mozilla Firefox"} # User-Agent headers to prevent request blocking    
DB_FILE = "quotes.db" # Database filename

# Logging config
LOG_FILE = "scraper.log"
LOG_LEVEL = logging.INFO

def setup_logging():
    """
    Configures logging for the application.
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        filename=LOG_FILE,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


