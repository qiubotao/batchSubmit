import unittest
from request_generator import RequestGenerator, generate_launchingnext_request
from website import Website

class TestRequestGenerator(unittest.TestCase):
    def setUp(self):
        self.website = Website(
            url="https://example.com",
            name="Test Tool",
            description="A test description",
            email="test@example.com",
            category="AI,Testing",
            user_name="Test User",
            pricing_model="free",
            user_first_name="Test",
            image_path="",
            content="",
            category_for_aitoolnet="",
            tags=["AI", "Testing"],
            funding_type="bootstrapped",
            board_members=False
        )
        
    def test_generate_post_request(self):
        generator = RequestGenerator()
        form_fields = {"test": "value"}
        code = generator.generate_post_request(
            url="https://example.com",
            form_fields=form_fields
        )
        
        # Verify code contains essential parts
        self.assertIn("import requests", code)
        self.assertIn("payload = {", code)
        self.assertIn("response = requests.post", code)
        self.assertIn("print(f'Status Code: {response.status_code}')", code)
        
    def test_extract_form_fields(self):
        generator = RequestGenerator()
        fields = generator.extract_form_fields(self.website)
        
        # Verify extracted fields
        self.assertEqual(fields["startupname"], "Test Tool")
        self.assertEqual(fields["email"], "test@example.com")
        self.assertEqual(fields["funding"], "bootstrapped")
        self.assertEqual(fields["board"], "no")
        
    def test_generate_launchingnext_request(self):
        code = generate_launchingnext_request(self.website)
        
        # Verify LaunchingNext-specific elements
        self.assertIn("https://www.launchingnext.com/submit/", code)
        self.assertIn('"Content-Type": "application/x-www-form-urlencoded"', code)
        self.assertIn("Mozilla/5.0", code)

if __name__ == '__main__':
    unittest.main()
