from website import Website
from launchingnext_adapter import LaunchingNextAdapter
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_submission():
    # Create a test website
    website = Website(
        url="https://example.com",
        name="Test AI Tool",
        description="A comprehensive AI tool for testing purposes. This tool helps developers automate their testing workflows.",
        email="test@example.com",
        category="AI,Testing,Development",
        user_name="Test User",
        pricing_model="free",
        user_first_name="Test",
        image_path="",
        content="",
        category_for_aitoolnet="",
        tags=["AI", "Testing", "Development"],
        funding_type="bootstrapped",
        board_members=False
    )
    
    try:
        # Create adapter instance
        adapter = LaunchingNextAdapter(website)
        
        # Run in headless mode for automated testing, switch to non-headless for captcha
        logger.info("Starting submission process...")
        try:
            # First attempt with headless mode
            adapter.submit(headless=True)
        except Exception as e:
            if "captcha" in str(e).lower():
                logger.info("Captcha detected - switching to interactive mode...")
                # Try again in non-headless mode for captcha
                adapter.submit(headless=False)
            else:
                raise
        
    except Exception as e:
        logger.error(f"Error during submission: {str(e)}")
        raise

if __name__ == "__main__":
    test_submission()
