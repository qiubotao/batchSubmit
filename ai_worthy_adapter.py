from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from submission_adapter import SubmissionAdapter
import time

class AIWorthyAdapter(SubmissionAdapter):
    def submit(self, headless=False):
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')

        
        # 默认打开控制台
        options.add_argument('--auto-open-devtools-for-tabs')
        
        
        driver_path = ChromeDriverManager(driver_version="128.0.6613.114").install()
        service = Service(driver_path)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        print("正在打开 AI Worthy 提交页面...")
        driver.get('https://aiworthy.org/submit-tool/')

        try:
            print("等待页面加载...")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

            print("页面已加载，正在填写表单...")

            # 填写表单字段
            self._fill_form_field(driver, 'input[name="your-name"]', self.website.user_name, "您的名字")
            self._fill_form_field(driver, 'input[name="your-email"]', self.website.email, "您的邮箱")
            self._fill_form_field(driver, 'input[name="tool-name"]', self.website.name, "工具名称")
            self._fill_form_field(driver, 'input[name="tool-url"]', self.website.url, "工具 URL")
            self._fill_form_field(driver, 'textarea[name="tool-description"]', self.website.description, "工具描述")

            print("表单填写完成")

            # 提交表单
            self._submit_form(driver)

            # 等待并捕获结果
            self._capture_submission_result(driver)

            input("请检查提交结果，按回车键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {str(e)}")
        finally:
            print("正在关闭浏览器...")
            driver.quit()

    def _fill_form_field(self, driver, selector, value, field_name):
        try:
            field = driver.find_element(By.CSS_SELECTOR, selector)
            field.clear()
            field.send_keys(value)
            print(f"已填写 '{field_name}' 字段")
        except Exception as e:
            print(f"填写 '{field_name}' 字段时出错: {str(e)}")

    def _submit_form(self, driver):
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            submit_button.click()
            print("表单已提交")
        except Exception as e:
            print(f"提交表单时出错: {str(e)}")

    def _capture_submission_result(self, driver):
        print("等待提交结果...")
        try:
            # 等待响应消息出现
            response_output = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wpcf7-response-output'))
            )
            print(f"提交结果: {response_output.text}")

            if "Thank you for your message" in response_output.text:
                print("提交成功！")
            else:
                print("提交可能未成功，请检查结果消息。")

        except Exception as e:
            print(f"捕获提交结果时出错: {str(e)}")

        # 额外的检查
        print("当前页面 URL:", driver.current_url)
        print("页面标题:", driver.title)

        # 检查是否有任何错误消息
        error_messages = driver.find_elements(By.CLASS_NAME, 'wpcf7-not-valid-tip')
        if error_messages:
            print("发现错误消息:")
            for error in error_messages:
                print(error.text)
        
        # 捕获并打印任何 JavaScript 控制台日志
        logs = driver.get_log('browser')
        if logs:
            print("浏览器控制台日志:")
            for log in logs:
                print(log)
