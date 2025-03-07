import unittest
from unittest.mock import patch, MagicMock
import requests
from quote_scraper.scraper import fetch_page, scrape_quotes, fetch_author_details
from quote_scraper.config import BASE_URL, HEADERS

class TestScraperFunctions(unittest.TestCase):
    @patch('quote_scraper.scraper.requests.get')
    def test_fetch_page_success(self, mock_get):
        """Test fetch_page() returns the expected HTML content on a successful request."""
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.text = "<html><body>Fake page content</body></html>"
        fake_response.raise_for_status = MagicMock()
        mock_get.return_value = fake_response
        
        url = "http://example.com"
        result = fetch_page(url)
        self.assertEqual(result, fake_response.text)
        mock_get.assert_called_once_with(url, headers=HEADERS)

    @patch('quote_scraper.scraper.requests.get')
    def test_fetch_page_failure(self, mock_get):
        """Test fetch_page() returns None when a RequestException occurs."""
        mock_get.side_effect = requests.RequestException("Error occurred")
        result = fetch_page("http://example.com")
        self.assertIsNone(result)

    @patch('quote_scraper.scraper.sleep', return_value=None)  # bypass delay in tests
    @patch('quote_scraper.scraper.fetch_page')
    def test_scrape_quotes_success(self, mock_fetch_page, mock_sleep):
        """Test scrape_quotes() extracts quotes correctly from HTML."""

        fake_html_page1 = """
            <html>
                <body>
                    <div class="quote">
                        <span class="text">"Quote 1"</span>
                        <span class="author">Author 1</span>
                        <a href="/bio/1"></a>
                    </div>
                    <div class="quote">
                        <span class="text">"Quote 2"</span>
                        <span class="author">Author 2</span>
                        <a href="/bio/2"></a>
                    </div>
                    <div class="next">
                        <a href="/page/2">Next</a>
                    </div>
                </body>
            </html>
        """

        fake_html_page2 = """
            <html>
                <body>
                    <div class="quote">
                        <span class="text">"Quote 3"</span>
                        <span class="author">Author 3</span>
                        <a href="/bio/3"></a>
                    </div>
                </body>
            </html>
        """
        mock_fetch_page.side_effect = [fake_html_page1, fake_html_page2]
        
        quotes = scrape_quotes()
        expected_quotes = [
            {"text": '"Quote 1"', "author": "Author 1", "bio_link": "/bio/1"},
            {"text": '"Quote 2"', "author": "Author 2", "bio_link": "/bio/2"},
            {"text": '"Quote 3"', "author": "Author 3", "bio_link": "/bio/3"}
        ]
        self.assertEqual(quotes, expected_quotes)
        self.assertEqual(mock_fetch_page.call_count, 2)

    @patch('quote_scraper.scraper.fetch_page')
    def test_fetch_author_details_success(self, mock_fetch_page):
        """Test fetch_author_details() returns correct details from valid HTML."""
        fake_html = """
            <html>
                <body>
                    <span class="author-born-date">January 1, 2000</span>
                    <span class="author-born-location">in Test City</span>
                </body>
            </html>
        """
        mock_fetch_page.return_value = fake_html
        birth_date, birth_place = fetch_author_details("/bio/test")
        self.assertEqual(birth_date, "January 1, 2000")
        self.assertEqual(birth_place, "in Test City")

    @patch('quote_scraper.scraper.fetch_page')
    def test_fetch_author_details_failure(self, mock_fetch_page):
        """Test fetch_author_details() returns (None, None) when details cannot be extracted."""
        fake_html = "<html><body></body></html>"
        mock_fetch_page.return_value = fake_html
        birth_date, birth_place = fetch_author_details("/bio/test")
        self.assertIsNone(birth_date)
        self.assertIsNone(birth_place)

if __name__ == '__main__':
    unittest.main()
