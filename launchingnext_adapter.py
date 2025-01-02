from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import traceback
from submission_adapter import SubmissionAdapter
import time
import logging
import json

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
    
    def submit(self, headless=False):
        driver = None
        try:
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

            # Handle funding type radio buttons with inspection results
            if self.website.funding_type:
                try:
                    funding_type = self.website.funding_type.lower()
                    logger.info(f"Attempting to select funding type: {funding_type}")
                    
                    # Find radio button by various attributes and parent text
                    script = """
                        var funding = arguments[0];
                        var radios = document.querySelectorAll('input[type="radio"]');
                        for (var radio of radios) {
                            var parent = radio.parentElement;
                            var text = parent ? parent.textContent.toLowerCase() : '';
                            if (radio.value.toLowerCase().includes(funding) ||
                                radio.name.toLowerCase().includes(funding) ||
                                text.includes(funding)) {
                                return radio;
                            }
                        }
                        return null;
                    """
                    funding_radio = driver.execute_script(script, funding_type)
                    if funding_radio:
                        driver.execute_script("arguments[0].click();", funding_radio)
                        logger.info(f"Successfully selected funding type: {funding_type}")
                    else:
                        logger.error(f"Could not find radio button for funding type: {funding_type}")
                except Exception as e:
                    logger.error(f"Failed to select funding type: {str(e)}")

            # Handle board members radio button with inspection results
            try:
                board_value = "yes" if self.website.board_members else "no"
                logger.info(f"Attempting to select board value: {board_value}")
                
                # Find radio button by various attributes and parent text
                script = """
                    var board = arguments[0];
                    var radios = document.querySelectorAll('input[type="radio"]');
                    for (var radio of radios) {
                        var parent = radio.parentElement;
                        var text = parent ? parent.textContent.toLowerCase() : '';
                        if (radio.value.toLowerCase().includes(board) ||
                            radio.name.toLowerCase().includes('board') ||
                            text.includes('board')) {
                            return radio;
                        }
                    }
                    return null;
                """
                board_radio = driver.execute_script(script, board_value)
                if board_radio: 
                    driver.execute_script("arguments[0].click();", board_radio)
                    logger.info(f"Successfully selected board value: {board_value}")
                else:
                    logger.error(f"Could not find radio button for board value: {board_value}")
            except Exception as e:
                logger.error(f"Failed to select board members: {str(e)}")

            logger.info("Form fields completed")

            # Handle math captcha
            self._handle_math_captcha(driver)

            # Submit form
            self._submit_form(driver)

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

    def _handle_math_captcha(self, driver):
        """Handle the math captcha field with user assistance."""
        try:
            # Wait for captcha element
            captcha_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="math_captcha"]'))
            )
            
            # Get captcha question text
            captcha_label = driver.find_element(By.CSS_SELECTOR, 'label[for="math_captcha"]')
            captcha_question = captcha_label.text.strip()
            
            # Try to parse and solve simple arithmetic
            try:
                # Extract numbers and operation from question (e.g., "What is 5 + 3?")
                import re
                numbers = re.findall(r'\d+', captcha_question)
                operation = re.search(r'[\+\-\*\/]', captcha_question)
                
                if len(numbers) == 2 and operation:
                    num1, num2 = map(int, numbers)
                    op = operation.group()
                    
                    if op == '+':
                        answer = num1 + num2
                    elif op == '-':
                        answer = num1 - num2
                    elif op == '*':
                        answer = num1 * num2
                    elif op == '/' and num2 != 0:
                        answer = num1 / num2
                    else:
                        raise ValueError("Unsupported operation")
                        
                    captcha_solution = str(int(answer))
                else:
                    raise ValueError("Could not parse captcha")
                    
            except Exception as e:
                logger.warning(f"Could not automatically solve captcha: {str(e)}")
                # Fallback to user input
                logger.info(f"Captcha question: {captcha_question}")
                captcha_solution = input("Please solve the math captcha: ")
            
            # Fill in the captcha solution
            self._fill_form_field(driver, 'input[name="math_captcha"]', captcha_solution, "Math Captcha")
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
