from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import traceback
from submission_adapter import SubmissionAdapter
from scraper_util import extract_website_info
from request_generator import generate_launchingnext_request
import time
import logging
import json
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LaunchingNextAdapter(SubmissionAdapter):
    """LaunchingNext submission adapter with enhanced URL verification.
    
    This adapter handles form submissions to LaunchingNext.com with multiple layers
    of URL verification:
    
    1. Initial Navigation:
       - Navigates directly to https://www.launchingnext.com/submit/
       - This is the known submission endpoint based on site structure
    
    2. Form Action Verification:
       - Checks the form's action attribute after page load
       - Logs warnings if action URL doesn't match expected pattern
       - Helps detect if site structure changes
    
    3. Network Request Monitoring:
       - Monitors actual form submission requests
       - Verifies POST requests go to expected endpoint
       - Provides debugging information for submission issues
    
    Expected Results:
    - Form should be found at /submit/ endpoint
    - Form action should contain 'launchingnext.com/submit'
    - POST request should be sent to same domain
    
    Warnings will be logged if:
    - Form action doesn't match expected pattern
    - Actual submission URL differs from expected
    - Network request monitoring fails
    """
    
    def _scrape_and_populate_fields(self):
        """
        Use scraper utility to fetch and populate missing website fields.
        """
        try:
            logger.info(f"Scraping website data from {self.website.url}...")
            scraped_data = extract_website_info(self.website.url)
            
            # Populate missing fields with scraped data
            if scraped_data.get('title') and not self.website.name:
                self.website.name = scraped_data['title']
                logger.info(f"Populated name from scraped title: {self.website.name}")
            
            if scraped_data.get('description') and not self.website.description:
                self.website.description = scraped_data['description']
                logger.info(f"Populated description from scraped data")
            
            if scraped_data.get('category') and not self.website.category:
                self.website.category = scraped_data['category']
                logger.info(f"Populated category from scraped data: {self.website.category}")
            elif scraped_data.get('tags') and not self.website.category:
                self.website.category = ', '.join(scraped_data['tags'])
                logger.info(f"Populated category from scraped tags: {self.website.category}")
            
            if scraped_data.get('funding_type') and not self.website.funding_type:
                self.website.funding_type = scraped_data['funding_type']
                logger.info(f"Populated funding type from scraped data: {self.website.funding_type}")
                
        except Exception as e:
            logger.error(f"Error during website scraping: {str(e)}")
            logger.debug(traceback.format_exc())

    def submit(self, headless=False):
        driver = None
        try:
            # Try to populate missing fields from website content
            self._scrape_and_populate_fields()
            
            logger.info("Initializing Chrome WebDriver...")
            options = webdriver.ChromeOptions()
            
            # Basic options for stability
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Headless specific configurations
            if headless:
                options.add_argument('--headless=new')
                options.add_argument('--disable-software-rasterizer')
                options.add_argument('--disable-extensions')
            
            # Create a temporary user data directory
            import tempfile
            import os
            user_data_dir = os.path.join(tempfile.gettempdir(), f'chrome_user_data_{os.getpid()}')
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # Add user agent to appear more like a real browser
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
            
            # Additional stability options
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            if headless:
                options.add_argument('--headless=new')
            else:
                options.add_argument('--auto-open-devtools-for-tabs')
            
            # Initialize Chrome WebDriver with performance logging
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            logger.info("Setting page load timeout...")
            driver.set_page_load_timeout(30)
            
            logger.info("Opening LaunchingNext submission page...")
            driver.get('https://www.launchingnext.com/submit/')
            
            logger.info("Waiting for page to load...")
            form_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, 'form'))
            )
            logger.info("Page loaded successfully")

            # Verify form action URL
            form_action = form_element.get_attribute('action')
            logger.info(f"Form action URL found: {form_action}")
            
            if not form_action or "launchingnext.com/submit" not in form_action.lower():
                logger.warning(f"Form action URL ({form_action}) does not match expected submission endpoint")
                logger.warning("Expected URL pattern: https://www.launchingnext.com/submit/")

            logger.info("Page loaded, filling form fields...")

            # Fill text fields
            self._fill_form_field(driver, 'input[name="startupname"]', self.website.name, "Startup Name")
            self._fill_form_field(driver, 'input[name="startupurl"]', self.website.url, "Startup URL")
            self._fill_form_field(driver, 'input[name="description"]', self.website.description[:200], "Headline")  # Limit to 200 chars
            self._fill_form_field(driver, 'textarea[name="fulldescription"]', self.website.description, "Full Description")
            self._fill_form_field(driver, 'input[name="tags"]', self.website.category, "Tags")
            self._fill_form_field(driver, 'input[name="user"]', self.website.user_name, "User Name")
            self._fill_form_field(driver, 'input[name="email"]', self.website.email, "Email")

            # Debug: Log all radio buttons on the page
            logger.info("Inspecting all radio buttons on the page...")
            radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            for radio in radio_buttons:
                try:
                    attrs = driver.execute_script("""
                        var items = {};
                        for (var i = 0; i < arguments[0].attributes.length; i++) {
                            var attr = arguments[0].attributes[i];
                            items[attr.name] = attr.value;
                        }
                        return items;
                    """, radio)
                    logger.info(f"Found radio button: {attrs}")
                    
                    # Get parent element text if available
                    parent_text = driver.execute_script("""
                        var element = arguments[0];
                        var parent = element.parentElement;
                        return parent ? parent.textContent.trim() : '';
                    """, radio)
                    if parent_text:
                        logger.info(f"Radio button parent text: {parent_text}")
                except Exception as e:
                    logger.error(f"Error inspecting radio button: {str(e)}")

            # Handle funding type radio button
            if self.website.funding_type:
                try:
                    funding_value = str(self.website.funding_type)  # e.g. "2"
                    radio = driver.find_element(By.CSS_SELECTOR, f'input[name="funding"][type="radio"][text="{funding_value}"]')
                    radio.click()
                    logger.info(f"Selected funding type: {funding_value}")
                except Exception as e:
                    logger.error(f"Failed to select funding type: {str(e)}")

            # Handle board members radio button
            try:
                board_value = "1" if self.website.board_members else "0"
                radio = driver.find_element(By.CSS_SELECTOR, f'input[name="boardmembers"][type="radio"][text="{board_value}"]')
                radio.click()
                logger.info(f"Selected board members: {board_value}")
            except Exception as e:
                logger.error(f"Failed to select board members: {str(e)}")

            logger.info("Form fields completed")

            # Generate and log POST request snippet for debugging
            try:
                request_snippet = generate_launchingnext_request(self.website)
                logger.info("Generated POST request snippet for debugging:")
                logger.info(request_snippet)
            except Exception as e:
                logger.error(f"Error generating request snippet: {str(e)}")
                logger.debug(traceback.format_exc())

            # Handle math captcha (known to be "2+3")
            logger.info("Handling math captcha...")
            captcha_field = driver.find_element(By.CSS_SELECTOR, 'input[name="math"]')
            captcha_field.clear()
            captcha_field.send_keys("5")
            logger.info("Math captcha filled")

            # Submit form
            logger.info("Submitting form...")
            submit_button = driver.find_element(By.CSS_SELECTOR, 'input[name="formSubmit"]')
            submit_button.click()
            logger.info("Form submitted")

            # Monitor network requests
            logger.info("Checking network requests...")
            logs = driver.get_log('performance')
            for entry in logs:
                try:
                    log = json.loads(entry['message'])['message']
                    if 'Network.requestWillBeSent' == log['method']:
                        request_url = log['params']['request']['url']
                        if 'submit' in request_url.lower():
                            logger.info(f"Detected form submission request to: {request_url}")
                            if "launchingnext.com/submit" not in request_url.lower():
                                logger.warning(f"Actual submission URL ({request_url}) differs from expected pattern")
                except Exception as e:
                    logger.debug(f"Error parsing network log: {str(e)}")

            # Check submission result
            self._check_submission_result(driver)

        except Exception as e:
            logger.error(f"Error during submission: {str(e)}")
        finally:
            if driver:
                logger.info("Closing browser...")
                try:
                    driver.quit()
                except Exception as e:
                    logger.error(f"Error closing browser: {str(e)}")
                    # Ensure the process is terminated
                    import os
                    import signal
                    try:
                        if hasattr(driver, 'service') and driver.service.process:
                            os.kill(driver.service.process.pid, signal.SIGTERM)
                    except Exception as kill_error:
                        logger.error(f"Error killing browser process: {str(kill_error)}")

    def _fill_form_field(self, driver, selector, value, field_name):
        """Fill a form field with the given value."""
        try:
            # Try different selector strategies
            selectors = [
                (By.CSS_SELECTOR, selector),  # Original selector
                (By.NAME, field_name.lower().replace(' ', '')),  # Try name attribute
                (By.ID, field_name.lower().replace(' ', '')),    # Try ID attribute
                (By.CSS_SELECTOR, f'input[placeholder*="{field_name}"]'),  # Try placeholder
                (By.CSS_SELECTOR, f'textarea[placeholder*="{field_name}"]')  # Try textarea
            ]
            
            field = None
            for by, sel in selectors:
                try:
                    field = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((by, sel))
                    )
                    break
                except:
                    continue
            
            if field is None:
                raise Exception(f"Could not find field {field_name} with any selector")
                
            field.clear()
            field.send_keys(value)
            logger.info(f"Successfully filled field {field_name}")
        except Exception as e:
            logger.error(f"Error filling '{field_name}' field: {str(e)}")

    def _select_radio_button(self, driver, value):
        """Select a radio button based on its value."""
        try:
            # Try different selector strategies for radio buttons
            selectors = [
                (By.CSS_SELECTOR, f'input[type="radio"][value="{value}"]'),
                (By.CSS_SELECTOR, f'input[type="radio"][name*="{value}"]'),
                (By.XPATH, f'//input[@type="radio" and @value="{value}"]'),
                (By.XPATH, f'//label[contains(text(), "{value}")]/input[@type="radio"]'),
                (By.XPATH, f'//label[contains(., "{value}")]/input[@type="radio"]')
            ]
            
            radio = None
            for by, selector in selectors:
                try:
                    radio = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    break
                except:
                    continue
            
            if radio is None:
                raise Exception(f"Could not find radio button {value} with any selector")
            
            if not radio.is_selected():
                # Try JavaScript click if regular click fails
                try:
                    radio.click()
                except:
                    driver.execute_script("arguments[0].click();", radio)
                    
            logger.info(f"Successfully selected radio button {value}")
        except Exception as e:
            logger.error(f"Error selecting radio button '{value}': {str(e)}")

    def _submit_form(self, driver):
        """Submit the form."""
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'input[name="formSubmit"]')
            submit_button.click()
            logger.info("Form submitted")
        except Exception as e:
            logger.error(f"Error submitting form: {str(e)}")

    def _handle_math_captcha(self, driver):
        """Handle the math captcha field (known to be 2+3=5)."""
        try:
            captcha_field = driver.find_element(By.CSS_SELECTOR, 'input[name="math"]')
            captcha_field.clear()
            captcha_field.send_keys("5")
            logger.info("Math captcha handled")
        except Exception as e:
            logger.error(f"Error handling math captcha: {str(e)}")
            raise

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
