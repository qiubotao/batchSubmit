from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LaunchingNextAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # Default open console for debugging
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        logger.info("Opening LaunchingNext submission page...")
        driver.get('https://www.launchingnext.com/submit/')

        try:
            logger.info("Waiting for page to load...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

            logger.info("Page loaded, filling form fields...")

            # Fill text fields
            self._fill_form_field(driver, 'input[name="startupname"]', self.website.name, "Startup Name")
            self._fill_form_field(driver, 'input[name="startupurl"]', self.website.url, "Startup URL")
            self._fill_form_field(driver, 'input[name="description"]', self.website.description[:200], "Headline")  # Limit to 200 chars
            self._fill_form_field(driver, 'textarea[name="fulldescription"]', self.website.description, "Full Description")
            self._fill_form_field(driver, 'input[name="tags"]', self.website.category, "Tags")
            self._fill_form_field(driver, 'input[name="user"]', self.website.user_name, "User Name")
            self._fill_form_field(driver, 'input[name="email"]', self.website.email, "Email")

            # Handle funding type radio buttons
            if self.website.funding_type:
                self._select_radio_button(driver, self.website.funding_type)

            # Handle board members radio button
            board_value = "yes" if self.website.board_members else "no"
            self._select_radio_button(driver, f"board_{board_value}")

            logger.info("Form fields completed")

            # Submit form
            self._submit_form(driver)

            # Check submission result
            self._check_submission_result(driver)

        except Exception as e:
            logger.error(f"Error during submission: {str(e)}")
        finally:
            logger.info("Closing browser...")
            driver.quit()

    def _fill_form_field(self, driver, selector, value, field_name):
        """Fill a form field with the given value."""
        try:
            field = driver.find_element(By.CSS_SELECTOR, selector)
            field.clear()
            field.send_keys(value)
            logger.info(f"Filled '{field_name}' field")
        except Exception as e:
            logger.error(f"Error filling '{field_name}' field: {str(e)}")

    def _select_radio_button(self, driver, value):
        """Select a radio button based on its value."""
        try:
            radio = driver.find_element(By.CSS_SELECTOR, f'input[type="radio"][value="{value}"]')
            if not radio.is_selected():
                radio.click()
            logger.info(f"Selected radio button with value '{value}'")
        except Exception as e:
            logger.error(f"Error selecting radio button '{value}': {str(e)}")

    def _submit_form(self, driver):
        """Submit the form."""
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            
            # Scroll to make button visible
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # Wait for button to be clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
            
            # Click using JavaScript
            driver.execute_script("arguments[0].click();", submit_button)
            
            logger.info("Form submitted")
        except Exception as e:
            logger.error(f"Error submitting form: {str(e)}")

    def _check_submission_result(self, driver):
        """Check if the submission was successful."""
        try:
            # Wait for success message or error
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.success-message, .error-message'))
            )
            
            # Check for success message
            success_messages = driver.find_elements(By.CSS_SELECTOR, '.success-message')
            if success_messages:
                logger.info("Submission successful")
            else:
                # Check for error message
                error_messages = driver.find_elements(By.CSS_SELECTOR, '.error-message')
                if error_messages:
                    logger.error(f"Submission failed: {error_messages[0].text}")
                else:
                    logger.warning("No success or error message found")
        except Exception as e:
            logger.error(f"Error checking submission result: {str(e)}")
