import unittest
from unittest.mock import patch, MagicMock
from quote_scraper import fetch_page, scrape_quotes, fetch_author_details 

class TestScraper(unittest.TestCase):

    @patch("scraper.requests.get")
    def test_fetch_page_success(self, mock_get):
        """
        Test fetch_page() when the request is successful.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Mock Page</body></html>"
        mock_get.return_value = mock_response

        result = fetch_page("http://mockurl.com")
        self.assertEqual(result, "<html><body>Mock Page</body></html>")

    @patch("scraper.requests.get")
    def test_fetch_page_failure(self, mock_get):
        """
        Test fetch_page() when the request fails.
        """
        mock_get.side_effect = Exception("Request failed")
        result = fetch_page("http://mockurl.com")
        self.assertIsNone(result)


    @patch("scraper.fetch_page")
    def test_scrape_quotes(self, mock_fetch_page):
        """
        Test scrape_quotes() to make sure they extract quotes correctly.
        """
        mock_fetch_page.return_value = '''
        <html>
            <body>
                <div>
                    <span class="text">"Mock Quote"</span>
                    <span class="author">Mock Author</span>
                    <a href="/mock-bio"></a>
                </div>
            </body>
        </html>
        '''
        expected_result = [{"text": '"Mock Quote"', "author": "Mock Author", "bio_link": "/mock-bio"}]

        result = scrape_quotes()
        self.assertEqual(result, expected_result)

        # to do: more tests


        