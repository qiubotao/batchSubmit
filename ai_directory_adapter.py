from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AiDirectoryAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AI Directory 提交页面...")
        driver.get('https://www.aidirectory.org/user-submit/')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'wpuf-form')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, '#post_title_934', self.website.name, "Post Title")
            
            # 选择分类
            self._select_form_field(driver, '#category', "Video ACR", "Category")  # 根据实际分类调整
            
            # 填写公司信息
            self._fill_form_field(driver, '#company_name_934', self.website.name, "Company Name")
            self._fill_form_field(driver, '#website_address_934', self.website.url, "Website Address")
            
            # 可选字段
            # self._fill_form_field(driver, '#street_934', "", "Street")
            # self._fill_form_field(driver, '#city_934', "", "City")
            # self._fill_form_field(driver, '#state_934', "", "State")
            # self._fill_form_field(driver, '#zip_code_934', "", "Zip Code")
            # self._fill_form_field(driver, '#country_934', "", "Country")
            
            # 必填字段
            self._fill_form_field(driver, '#phone_number_934', "1234567890", "Phone Number")  # 需要提供电话号码
            self._fill_form_field(driver, '#email_934', self.website.email, "Email")
            
            # 填写描述
            self._fill_form_field(driver, '#post_content_934', self.website.description, "Description")

            print("表单填写完成，等待验证码...")

            # 等待人工处理验证码
            time.sleep(30)  # 给用户30秒时间处理验证码

            # 提交表单
            self._submit_form(driver)

            # 等待并检查提交结果
            self._capture_submission_result(driver)
            self._check_submission_success(driver)

        except Exception as e:
            print(f"提交表单时出错: {str(e)}")
        finally:
            if not headless:
                time.sleep(5)  # 给一些时间查看结果
            driver.quit()

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.CLASS_NAME, 'wpuf-submit-button')
            if not submit_button.is_enabled():
                print("提交按钮未启用，可能需要完成验证码")
                return
            submit_button.click()
            print("已点击提交按钮")
        except Exception as e:
            print(f"点击提交按钮时出错: {str(e)}")

    def _capture_submission_result(self, driver):
        print("等待页面响应...")
        time.sleep(5)

        try:
            # 检查可能的成功或错误消息
            messages = driver.find_elements(By.CSS_SELECTOR, '.wpuf-success, .wpuf-error, .wpuf-message')
            for message in messages:
                print("提交结果消息:", message.text)
        except Exception as e:
            print(f"检查提交结果时出错: {str(e)}")

    def _check_submission_success(self, driver):
        try:
            success_elements = driver.find_elements(By.CSS_SELECTOR, '.wpuf-success')
            if success_elements:
                print("提交成功")
                return True
            print("未检测到成功提交的标志")
            return False
        except Exception as e:
            print(f"检查提交状态时出错: {str(e)}")
            return False

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            element.clear()
            element.send_keys(value)
            print(f"已填写 {field_name}: {value}")
        except Exception as e:
            print(f"填写 {field_name} 时出错: {str(e)}")

    def _select_form_field(self, driver, selector, value, field_name):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            for option in element.find_elements(By.TAG_NAME, 'option'):
                if option.text == value:
                    option.click()
                    print(f"已选择 {field_name}: {value}")
                    break
        except Exception as e:
            print(f"选择 {field_name} 时出错: {str(e)}")
