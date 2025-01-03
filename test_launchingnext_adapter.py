import unittest
from unittest.mock import patch, MagicMock
from launchingnext_adapter import LaunchingNextAdapter
from website import Website
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestLaunchingNextAdapter(unittest.TestCase):
    def setUp(self):
        self.website = Website(
            url="https://example.com",
            name="",  # Empty to test population
            description="",  # Empty to test population
            email="test@example.com",
            category="",  # Empty to test population
            user_name="Test User",
            pricing_model="free",
            user_first_name="Test",
            image_path="",
            content="",
            category_for_aitoolnet="",
            tags=[],
            funding_type="",  # Empty to test population
            board_members=False
        )
        self.adapter = LaunchingNextAdapter(self.website)

    @patch('scraper_util.requests.get')
    def test_scrape_and_populate_fields(self, mock_get):
        # Mock response with test HTML content
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <head>
                <title>Test AI Tool</title>
                <meta name="description" content="An amazing AI tool for testing">
                <meta name="keywords" content="AI, Testing, Automation">
            </head>
            <body>
                <div>This is a bootstrapped project</div>
            </body>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test scraping and field population
        self.adapter._scrape_and_populate_fields()

        # Verify fields were populated
        self.assertEqual(self.website.name, "Test AI Tool")
        self.assertEqual(self.website.description, "An amazing AI tool for testing")
        self.assertEqual(self.website.category, "AI, Testing, Automation")
        self.assertEqual(self.website.funding_type, "bootstrapped")

    @patch('scraper_util.requests.get')
    def test_scrape_error_handling(self, mock_get):
        # Test network error
        mock_get.side_effect = Exception("Network error")
        self.adapter._scrape_and_populate_fields()
        # Should not raise exception, just log error

    def test_request_snippet_generation(self):
        # Test request snippet generation
        self.website.name = "Test Tool"
        self.website.description = "Test Description"
        self.website.category = "AI, Testing"
        
        try:
            self.adapter._scrape_and_populate_fields()
            # Should not affect the test if scraping fails
        except Exception:
            pass

        # Submit form to generate request snippet (headless mode to avoid browser)
        with self.assertLogs(level='INFO') as log:
            try:
                self.adapter.submit(headless=True)
            except Exception:
                # We expect an exception since we're not completing the submission
                pass

            # Verify request snippet was generated and logged
            request_logs = [record.message for record in log.records if 'Generated POST request snippet' in record.message]
            self.assertTrue(any(request_logs), "Request snippet should be logged")

    @patch('selenium.webdriver.Chrome')
    def test_form_field_mappings(self, mock_chrome):
        # Mock the driver and its methods
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_element = MagicMock()
        mock_driver.find_element.return_value = mock_element

        # Set up test data
        self.website.name = "Test Startup"
        self.website.url = "https://example.com"
        self.website.description = "Short description"
        self.website.content = "Full description"
        self.website.category = "AI, Testing"
        self.website.user_name = "Test User"
        self.website.email = "test@example.com"
        self.website.funding_type = "2"  # Bootstrapped
        self.website.board_members = True

        # Try submitting the form
        self.adapter.submit(headless=True)

        # Verify each form field was filled correctly
        expected_calls = [
            ('css selector', 'input[name="startupname"]'),
            ('css selector', 'input[name="startupurl"]'),
            ('css selector', 'input[name="description"]'),
            ('css selector', 'textarea[name="fulldescription"]'),
            ('css selector', 'input[name="tags"]'),
            ('css selector', 'input[name="user"]'),
            ('css selector', 'input[name="email"]'),
            ('css selector', 'input[name="funding"][type="radio"][text="2"]'),
            ('css selector', 'input[name="boardmembers"][type="radio"][text="1"]'),
            ('css selector', 'input[name="math"]'),
            ('css selector', 'input[name="formSubmit"]')
        ]
        
        for by, selector in expected_calls:
            mock_driver.find_element.assert_any_call('css selector', selector)

    @patch('selenium.webdriver.Chrome')
    def test_math_captcha(self, mock_chrome):
        # Mock the driver and its methods
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_element = MagicMock()
        mock_driver.find_element.return_value = mock_element

        # Test math captcha handling
        self.adapter._handle_math_captcha(mock_driver)

        # Verify captcha field was found and filled with "5" (2+3)
        mock_driver.find_element.assert_called_with('css selector', 'input[name="math"]')
        mock_element.send_keys.assert_called_with("5")

    @patch('selenium.webdriver.Chrome')
    def test_radio_button_selection(self, mock_chrome):
        # Mock the driver and its methods
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_element = MagicMock()
        mock_driver.find_element.return_value = mock_element

        # Test funding type radio button
        self.website.funding_type = "2"  # Bootstrapped
        mock_driver.find_element.reset_mock()
        self.adapter.submit(headless=True)
        mock_driver.find_element.assert_any_call('css selector', 'input[name="funding"][type="radio"][text="2"]')

        # Test board members radio button
        self.website.board_members = True
        mock_driver.find_element.reset_mock()
        self.adapter.submit(headless=True)
        mock_driver.find_element.assert_any_call('css selector', 'input[name="boardmembers"][type="radio"][text="1"]')

if __name__ == '__main__':
    unittest.main()
