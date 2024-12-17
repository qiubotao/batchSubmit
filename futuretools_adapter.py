from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class FutureToolsAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 FutureTools 提交页面...")
        driver.get('https://www.futuretools.io/submit-a-tool')

        try:
            print("等待页面加载...")
            self._wait_for_page_load(driver)

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, '#name', self.website.user_name, "Your Name")
            self._fill_form_field(driver, '#email', self.website.email, "Email")
            self._fill_form_field(driver, '#Tool-Name', self.website.name, "Tool Name")
            self._fill_form_field(driver, '#Tool-URL', self.website.url, "Tool URL")
            self._fill_form_field(driver, '#Tags', self.website.category , "Tags")
            self._select_form_field(driver, '#Pricing-Model', "Freemium", "Pricing Model")
            self._fill_form_field(driver, '#Tool-Description', self.website.description, "Tool Description")
            self._fill_form_field(driver, '#Other-Details', "", "Other Details")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 检查提交是否成功
            self._check_submission_success(driver)

            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _wait_for_page_load(self, driver):
        try:
            # 等待表单加载完成
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'email-form'))
            )
            print("页面加载完成")
        except Exception as e:
            print(f"等待页面加载时出错: {str(e)}")
            raise

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _select_form_field(self, driver, selector, value, field_name):
        try:
            select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            option = select.find_element(By.CSS_SELECTOR, f'option[value="{value}"]')
            option.click()
            print(f"已选择 '{field_name}' 字段")
        except Exception as e:
            print(f"选择 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit-button'))
            )
            
            # 滚动到元素可见位置
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            
            # 使用 JavaScript 直接点击元素
            driver.execute_script("arguments[0].click();", submit_button)
            
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _check_submission_success(self, driver):
        try:
            # 检查是否重定向到感谢页面
            WebDriverWait(driver, 10).until(
                lambda d: 'tool-submission-thank-you' in d.current_url
            )
            print("提交成功")
        except Exception as e:
            print(f"检查提交成功时出错: {str(e)}")
